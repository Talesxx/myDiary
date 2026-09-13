# Canvas 性能优化

## 一、开销从哪里来

Canvas 2D 每一帧的耗时由三部分构成：

1. **路径构建与光栅化** —— 每个 `arc` / `lineTo` / `fill` 都要重新做几何计算和扫描线填充
2. **状态切换** —— `fillStyle` / `transform` / `globalAlpha` 的变更会打断内部的绘制批次
3. **像素填充** —— 开销与画布**面积**成正比，与 DPR 成**平方**关系

关键结论：第 3 项由分辨率决定，是最容易降的；第 1、2 项才是所谓"绘制优化"的主战场。所以优化的两条主线是——

- **少画**：把不变的内容缓存成位图，把同类的绘制合并成批次（第二、三节）
- **少帧**：帧预算不够时干脆不渲染这一帧（第四节）

---

## 二、双重画布

### 2.1 思路：动静分离

每帧都在重绘的东西，和从不变化的东西，拆到两张画布上。静态层只画一次，之后永远不动；动态层每帧只做 `clearRect` + 绘制自己那部分。

因为静态层的像素在两次重绘之间**被浏览器保留**，动态层重绘时它的开销是零。

### 2.2 方案 A：DOM 双 canvas 叠层

```html
<div class="stage">
  <canvas id="bg" class="layer"></canvas>
  <canvas id="fg" class="layer"></canvas>
</div>
```

```css
.stage { position: relative; }
.layer { position: absolute; inset: 0; }
```

```js
const bg = document.getElementById('bg')
const fg = document.getElementById('fg')

// 只执行一次
function paintBackground() {
  const ctx = bg.getContext('2d')
  setupHiDPI(ctx, bg, W, H)
  drawGrid(ctx)
  drawStaticDecor(ctx)
}

// 每帧只清前景层
function renderFrame(t) {
  const ctx = fg.getContext('2d')
  ctx.clearRect(0, 0, W, H)
  drawParticles(ctx, t)
  requestAnimationFrame(renderFrame)
}
```

`bg` 层**永不** `clearRect`，浏览器会把它作为一张常驻合成层保留下来，动态层重绘时背景层没有任何 GPU 开销。

代价是页面多一层合成、多一个 GPU 纹理。合成层数量有上限，叠到几十层反而会明显退化——只拆必要的两三层。

### 2.3 方案 B：离屏 Canvas 缓存

不需要动 DOM 结构，把静态内容画进一张内存画布，每帧一次 `drawImage` 贴回来：

```js
const cache = document.createElement('canvas')
cache.width = W * dpr
cache.height = H * dpr
const cctx = cache.getContext('2d')
cctx.scale(dpr, dpr)
drawGrid(cctx)                      // 构建静态位图

function render(ctx, t) {
  ctx.clearRect(0, 0, W, H)
  ctx.drawImage(cache, 0, 0, W, H)  // 一次位块传送，替代上千次路径操作
  drawParticles(ctx, t)
}
```

`drawImage` 走的是 GPU blit，比重新光栅化便宜一到两个数量级。

**尺寸陷阱**：`cache` 的 backing store 是 `W * dpr`，但当前 `ctx` 已经 `scale(dpr, dpr)` 过了，所以绘制时要传 CSS 尺寸 `W, H`。两处 DPR 处理不一致就会出现模糊或错位。

### 2.4 什么时候缓存反而更慢

缓存不是免费的，两种情况会倒亏：

- **显存成本**：一张画布的字节数 = `width × height × 4`。1000×1000 在 DPR=2 下是 `2000 × 2000 × 4 ≈ 16 MB`。缓存三四层就是几十 MB，移动端会触发纹理换出。
- **静态内容会变**：比如画布本身要平移、缩放，缓存就得整体重绘，这时不如直接画。

经验判据：**静态部分的重绘耗时超过约 2ms/帧，或路径数量达到数百个**，缓存开始划算。

### 2.5 OffscreenCanvas 与 Worker

上面的优化都还在主线程上跑。要彻底不阻塞主线程，把渲染搬进 Worker：

```js
// 主线程
const offscreen = canvas.transferControlToOffscreen()
const worker = new Worker('render.js')
worker.postMessage({ canvas: offscreen, dpr }, [offscreen])
```

```js
// render.js
self.onmessage = ({ data }) => {
  const ctx = data.canvas.getContext('2d')
  const loop = (t) => { draw(ctx, t); requestAnimationFrame(loop) }
  requestAnimationFrame(loop)
}
```

限制要提前知道：

- Worker 里没有 DOM，所有 `HTMLImageElement` 必须换成 `ImageBitmap`（`createImageBitmap(blob)`）
- `transferControlToOffscreen()` 是**一次性**的，调用后主线程再 `getContext` 会拿到 `null`
- Safari 对 Worker 内 rAF 的支持较晚（iOS 16.4 起才完整），需要保留降级分支

---

## 三、绘制优化

### 3.1 减少状态切换

Canvas 内部会把连续的绘制调用合批，`fillStyle` / `strokeStyle` / `transform` 一变就打断批次。所以应当**按状态分组，而不是按逻辑分组**：

```js
// 差：每画一个点就切一次样式
points.forEach(p => {
  ctx.fillStyle = p.color
  ctx.beginPath()
  ctx.arc(p.x, p.y, 2, 0, TAU)
  ctx.fill()
})

// 好：按颜色归组，一组一次 beginPath + 一次 fill
for (const [color, group] of groupBy(points, p => p.color)) {
  ctx.fillStyle = color
  ctx.beginPath()
  for (const p of group) {
    ctx.moveTo(p.x + 2, p.y)   // 断开子路径，避免 arc 之间连出直线
    ctx.arc(p.x, p.y, 2, 0, TAU)
  }
  ctx.fill()
}
```

`moveTo` 那一步不能省。`arc` 之间不 `moveTo` 的话，Canvas 会把上一条弧的终点和这一条弧的起点连起来，画出多余的直线。

### 3.2 用 Path2D 缓存路径

`Path2D` 是几何数据的"已编译"形式，可以构建一次、每帧复用：

```js
const star = new Path2D()
buildStarPath(star, 0, 0, 10)

// 每帧只换 transform，不再重建路径
for (const s of stars) {
  ctx.setTransform(dpr, 0, 0, dpr, s.x, s.y)
  ctx.fill(star)
}
ctx.setTransform(dpr, 0, 0, dpr, 0, 0)   // 复位
```

热循环里优先用 `setTransform` 而不是 `save() / translate() / restore()`，少一层状态栈操作。

### 3.3 代价高的 API

下面这些放在热循环里，就是掉帧的直接来源：

| API | 为什么慢 | 替代方案 |
| --- | --- | --- |
| `shadowBlur` / `shadowColor` | 每个图形额外一次高斯模糊，开销随半径增长很快 | 预渲染带阴影的精灵位图 |
| `filter`（blur / drop-shadow） | 同上，且强制离屏渲染 | 同上 |
| `globalCompositeOperation` | 打断批次，部分模式会强制读回 | 只在少量顶层元素上用 |
| `getImageData` / `putImageData` | GPU→CPU 回读，强制管线 flush，单次几到几十毫秒 | 移出热循环；确需频繁使用则在建 context 时加 `willReadFrequently: true` |
| `measureText` / `fillText` | 字形排版 + 光栅化，字体越复杂越慢 | 文字预渲染成位图，用 `drawImage` |

### 3.4 脏矩形重绘

全画布 `clearRect` 本身很便宜，贵的是**重绘整个画布的路径**。只重绘变化的区域：

```js
// dirty = 上一帧包围盒 ∪ 这一帧包围盒
ctx.save()
ctx.beginPath()
ctx.rect(dirty.x0, dirty.y0, dirty.x1 - dirty.x0, dirty.y1 - dirty.y0)
ctx.clip()
renderScene(ctx)
ctx.restore()
```

坑有两个：

- 只清"当前位置"会留下残影，必须清**上一帧和这一帧的并集**
- 脏矩形适合少数大对象移动（拖拽一个图形、局部刷新图表）；满屏粒子时包围盒几帧内就等于整屏，白付了 `clip` 的开销，反而更慢

### 3.5 避免每帧分配对象

GC 停顿是掉帧里最隐蔽的一种。热循环中不要 `map` / `filter` 产生新数组、不要创建闭包、不要解构大对象。粒子之类的用对象池：

```js
class Pool {
  constructor(n, make) {
    this.items = Array.from({ length: n }, make)
    this.free = n
  }
  spawn() { return this.free ? this.items[--this.free] : null }
  release(p) { this.items[this.free++] = p }
}
```

拿不到就**丢弃这个粒子**，而不是扩容——元素数量本身就应该是降级手段之一，不该随负载无限增长。

### 3.6 分辨率是第一杠杆

像素填充开销 ∝ 面积，而 DPR 是平方关系。DPR=3 的手机上，`canvas.width = cssW * 3` 意味着 9 倍像素量。

```js
const renderScale = Math.min(dpr, 2)   // 上限锁死 2 档

canvas.width  = cssW * renderScale
canvas.height = cssH * renderScale
canvas.style.width  = cssW + 'px'      // CSS 尺寸不变，浏览器负责放大
canvas.style.height = cssH + 'px'
```

这是**性价比最高的降级手段**：只降分辨率，不动任何绘制逻辑，帧率立刻回来，视觉上只是略微发糊。后面第 4.7 节的降级阶梯把它排在第一级。

---

## 四、rAF 性能不足时取消中间渲染

### 4.1 前提：让动画按时间步进

跳帧的前提是动画由**时间**驱动，而不是由**帧数**驱动。否则丢掉一帧，动画就慢一拍。

```js
let last = performance.now()

function loop(now) {
  requestAnimationFrame(loop)
  const dt = Math.min(now - last, 100)   // 钳制：见下
  last = now
  update(dt)                             // 状态推进用 dt，不用帧计数
  render()
}
requestAnimationFrame(loop)
```

`Math.min(dt, 100)` 这个钳制是必须的。标签页切到后台时 rAF 自动暂停，切回来 `dt` 可能是几万毫秒，不钳制的话画面会瞬移一大截，物理模拟甚至会直接炸开。

### 4.2 测量帧预算

60Hz 每帧预算 16.7ms，120Hz 只有 8.3ms。要留出约 30% 给浏览器自身的样式计算与合成：

```js
const BUDGET = 1000 / 60 * 0.7      // ≈ 11.7ms

let renderCost = 0                  // 上一帧实测耗时，用滑动平均避免抖动

function loop(now) {
  requestAnimationFrame(loop)
  const t0 = performance.now()
  update(dt)
  render()
  renderCost = renderCost * 0.8 + (performance.now() - t0) * 0.2
}
```

### 4.3 跳帧：主动丢弃中间帧

实测耗时一旦超出预算，**继续每帧渲染只会让每帧更迟**，形成正反馈恶化。此时应该主动跳过渲染，把时间还给浏览器：

```js
let skipCount = 0
const MAX_SKIP = 3                  // 最多连续跳 3 帧，防止彻底卡死

function loop(now) {
  requestAnimationFrame(loop)

  const dt = Math.min(now - last, 100)
  last = now
  update(dt)                        // 状态照常推进，动画不减速

  if (renderCost > BUDGET && skipCount < MAX_SKIP) {
    skipCount++
    return                          // 这一帧不画
  }
  skipCount = 0

  const t0 = performance.now()
  render()
  renderCost = renderCost * 0.8 + (performance.now() - t0) * 0.2
}
```

关键点：跳帧时 `update(dt)` **不能跳过**，并且这段时间要在下一帧的 `dt` 里累积回来——时间是真的流逝了。跳掉的只是"画"这一步，不是"算"这一步。

`MAX_SKIP` 也不能省。没有它的话，一旦渲染持续超支就会无限跳帧，画面直接冻住；有上限则保证再慢也能以极低帧率动起来，用户至少知道它没死。

### 4.4 更稳的做法：定频降级而非随机跳帧

随机跳帧的观感是抖动——一帧 16ms、下一帧 33ms。更好的策略是**明确降到 30fps**：节奏均匀，人眼对稳定 30fps 的接受度远高于忽快忽慢的 60fps。

```js
let frameInterval = 1000 / 60
let nextDue = 0

function loop(now) {
  requestAnimationFrame(loop)
  if (now < nextDue) return                  // 未到渲染时刻 → 丢弃这一帧

  if (now - nextDue > frameInterval * 3) {
    nextDue = now + frameInterval            // 落后太多（切后台回来），重新对齐
  } else {
    nextDue += frameInterval                 // 正常推进，无累积漂移
  }

  update(dt)
  render()
}

// 按实测耗时在档位之间切换
function adapt(renderCost) {
  if (renderCost > 1000 / 30 * 0.7) frameInterval = 1000 / 30
  else if (renderCost < 1000 / 60 * 0.5) frameInterval = 1000 / 60
}
```

### 4.5 脏标记：没有变化就不渲染

如果应用是**事件驱动**而非连续动画（图表、白板、拖拽），rAF 空转本身就是纯浪费。用脏标记合并中间状态：

```js
let dirty = false
const invalidate = () => { dirty = true }

function loop() {
  requestAnimationFrame(loop)
  if (!dirty) return          // 这一帧状态没变，直接不渲染
  dirty = false
  render()
}
```

这是"取消中间渲染"最贴近字面的一层含义：一秒内状态变了 100 次，若每次都立即渲染就要画 100 次；用脏标记合并后只画 60 次（受 rAF 上限约束），而且画的永远是最新状态——中间那 40 次渲染被**真正取消**了，不是延后执行，是不执行。

配套做法：图片解码、大数组排序这类耗时任务放 `requestIdleCallback`，不要占用渲染帧。

### 4.6 用 cancelAnimationFrame 真正取消待渲染的帧

`requestAnimationFrame` 只是把回调**排队**，在被调用之前它一直处于 pending 状态。`cancelAnimationFrame(id)` 能把这一帧从队列里摘掉，于是：

- 回调**不会被调用**
- 浏览器**不必为它做帧调度**

两点必须说明白，否则很容易用错：

1. 它取消的是**整帧**——`update` 和 `render` 一起没，做不到"只取消绘制但保留状态推进"
2. 回调一旦**开始执行**就取消不了了。对正在运行的回调调 `cancelAnimationFrame` 是空操作

由此得到两个 API 的分工：

| 想要的效果 | 手段 |
| --- | --- |
| 跳过**渲染**，状态照常推进 | 回调内 `return`（4.3 节） |
| 跳过**整帧**，连回调和调度一起省 | `cancelAnimationFrame`，不排或撤掉这个 id |

#### 用途一：真正停掉循环

4.5 节的脏标记是"空转但不渲染"，回调仍然每秒被调用 60 次，只是很快返回。事件驱动型应用可以更彻底——没有变化时一帧都不排：

```js
let rafId = null

function loop() {
  rafId = null          // 先清空，表示当前没有 pending 帧
  render()
  // 不在这里无条件排下一帧
}

function invalidate() {
  if (rafId !== null) return               // 已排队，不重复排
  rafId = requestAnimationFrame(loop)
}
```

外部只管调 `invalidate()`：空闲时零回调、零调度，比脏标记还省一层。而且 `if (rafId !== null) return` 这句顺带完成了合并——一秒内调 100 次 `invalidate`，只有第一次真正排队，其余 99 次是做一次判空就返回。**这就是中间渲染被取消的时刻**，它们从未进入队列。

#### 用途二：撤销过期帧，立即用最新状态重排

上面是"保留先到的、丢弃后到的"。反过来也行——新状态比排队时更新，就把旧的撤了重排：

```js
function invalidate() {
  if (rafId !== null) cancelAnimationFrame(rafId)   // 撤掉用旧状态排的那一帧
  rafId = requestAnimationFrame(loop)               // 用最新状态重新计时
}
```

两者渲染**次数**完全一样，差别在**时机**：

- 保留先到的 → 保证不晚于原定时刻出图，延迟更稳定
- 撤销重排 → 保证出图时用的是最新状态，但连续高频调用会把出图时刻一路往后推

拖动、缩放这类连续高频变更用后者（要的是最新状态）；定时轮播、固定节奏动画用前者（要的是准时）。

#### 用途三：模式切换与清理

从连续动画切到按需渲染、组件卸载、元素滚出视口——都必须显式取消。否则回调里访问已销毁的对象会报错，或者白白占着一个合成层：

```js
function stop() {
  if (rafId !== null) {
    cancelAnimationFrame(rafId)   // 对已执行的 id 调用是安全的空操作
    rafId = null
  }
}

document.addEventListener('visibilitychange', () => {
  document.hidden ? stop() : invalidate()
})
window.addEventListener('pagehide', stop)
```

可见性这里有个细节值得单独提：切到后台时浏览器本来就会暂停 rAF，主动取消并**没有**额外收益。真正的收益在**切回来时**——待执行的帧会带着一个几万毫秒的 `dt` 一起回来。要么像 4.1 节那样钳制 `dt`，要么像这里直接 `stop()` 掉、恢复时重新计时。后者更干净，因为它连"带病的那一帧"都不让它执行。

#### 陷阱：在回调开头排下一帧，就永远停不下来

```js
// 危险写法
function loop() {
  rafId = requestAnimationFrame(loop)   // 每次进来都先把下一帧排好
  if (done) return                      // 这个 return 只能跳过本次绘制
  render()                              // 循环本身永远不会终止
}
```

这是最常见的写法（好处是"排帧"和"绘制"耗时分开，不会被跳帧逻辑跳过），但它把循环变成自续的——要停必须显式取消刚排上的那个 id：

```js
function loop() {
  rafId = requestAnimationFrame(loop)
  if (done) {
    cancelAnimationFrame(rafId)   // 不取消就是死循环级别的空转
    rafId = null
    return
  }
  render()
}
```

另一种写法是把 `requestAnimationFrame` 挪到回调**末尾**，让"排下一帧"成为绘制成功的自然结果——不排就是不续，天然可停。但这样 4.3 节的跳帧逻辑位置就必须跟着改：

```js
function loop(now) {
  const dt = Math.min(now - last, 100)
  last = now
  update(dt)

  if (renderCost > BUDGET && skipCount < MAX_SKIP) {
    skipCount++
    requestAnimationFrame(loop)   // 跳帧也必须续排，否则整条循环在这里断掉
    return
  }
  skipCount = 0

  const t0 = performance.now()
  render()
  renderCost = renderCost * 0.8 + (performance.now() - t0) * 0.2
  requestAnimationFrame(loop)
}
```

**末尾排帧的坑就在这**：4.3 节那段跳帧代码原本是"直接 `return` 就完事"（因为开头已经排好了下一帧），照搬到这里就变成了"跳一帧 = 关停循环"。挪位置的时候这个 `return` 分支必须一起改。

两种写法都成立，选一种就别混用：

- **开头排帧** —— 跳帧逻辑干净（`return` 即可），但必须配 `cancelAnimationFrame` 才能停
- **末尾排帧** —— 天然可停、语义直白，但每个提前 `return` 的分支都要记得续排

### 4.7 降级阶梯

按代价从低到高逐级触发，**不要一步降到底**：

| 级别 | 手段 | 代价 | 收益 |
| --- | --- | --- | --- |
| 1 | 降渲染分辨率（renderScale 2 → 1） | 画面略糊 | ★★★ |
| 2 | 减少粒子 / 元素数量 | 内容变少 | ★★★ |
| 3 | 关阴影、关滤镜、关抗锯齿 | 细节丢失 | ★★ |
| 4 | 定频降到 30fps | 流畅度下降但节奏均匀 | ★★ |
| 5 | 跳帧 / 脏标记按需渲染 | 动画可能停顿 | ★ |
| 6 | 停止 rAF，静态兜底 | 退化为静态图 | 兜底 |

恢复要**滞后**：连续 2 秒稳定在预算内才回升一级，否则会在档位之间反复横跳，观感比一直待在低档还差。

---

## 五、检查清单

- [ ] 静态内容是否已缓存（离屏 canvas 或独立图层）？
- [ ] `fillStyle` 等状态是否按组批处理，而非逐元素切换？
- [ ] 热循环里是否还有 `shadowBlur` / `filter` / `getImageData`？
- [ ] 路径是否用 `Path2D` 缓存，而非每帧重建？
- [ ] DPR 是否处理正确，且分辨率已作为降级杠杆？
- [ ] `dt` 是否钳制？切标签页回来画面是否跳变？
- [ ] 有无脏标记？无变化时是否仍在空转渲染？
- [ ] 停止动画 / 组件卸载 / 切后台时，是否 `cancelAnimationFrame` 清理了？循环是否真的会停？
- [ ] 是否实测帧耗时并据此触发降级，而不是凭感觉？

## 六、测量方法

```js
let frames = 0
let mark = performance.now()

;(function tick() {
  requestAnimationFrame(tick)
  frames++
  const now = performance.now()
  if (now - mark >= 1000) {
    console.log(`FPS: ${frames}`)
    frames = 0
    mark = now
  }
})()
```

工具：

- DevTools → **Performance** 录制，看 Rendering 泳道的 Frame 与 GPU 耗时分布
- DevTools → **Rendering** 面板勾选 **Frame Rendering Stats**，实时观察 fps 与 GPU 显存占用
- 一定要在真机上测。移动端 GPU 填充率常常只有桌面的十分之一，桌面 Chrome 上的流畅证明不了任何事
