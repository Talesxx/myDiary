# ts导出问题

请在项目中或包开发中正确的导出

- 如 interface type 请使用export type导出，部分脚手架可能无法识别不正确的导出.
- `尤其是包开发中这可能导致使用者无法使用.`
```ts
// interface type 请使用export type导出
export type { XXXinterface, XXXtype }; // 正确示范
// 不要使用 此方法导出。在其他项目导入时， 
// 此方法导出可能 部分脚手架过程无法正确识别这只是ts的类型，
// 而是去查找.js文件中的导出从而报错
export { XXXinterface, XXXtype }; // 错误示范
```