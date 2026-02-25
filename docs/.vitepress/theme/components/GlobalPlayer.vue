<template>
  <div class="global-player-wrapper">
    <div id="global-player" ref="playerRef"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import 'aplayer/dist/APlayer.min.css'
//获取当前页面的baseURL路径，用于拼接音频地址
const BaseURL = import.meta.env.BASE_URL;
const playerRef = ref<HTMLElement>()
let player: any | null = null

onMounted(async () => {
  if (playerRef.value) {
    // @ts-ignore 
    const APlayer = (await import('aplayer')).default
    // 在客户端环境中获取基础URL
    const clientBaseUrl = typeof window !== 'undefined' ? window.location.origin + BaseURL : BaseURL;
    // 配置音乐列表
    const options = {
      container: playerRef.value,
      fixed: true,
      mini: true,
      autoplay: false,
      theme: '#b7daff',
      loop: 'all',
      order: 'random',
      preload: 'auto',
      volume: 0.5,
      mutex: true,
      listFolded: true,
      listMaxHeight: '250px',
      lrcType: 3,
      audio: [
        {
          name: '不得不爱',
          artist: 'AI心夏',
          url: clientBaseUrl + '/audio/【AI心夏】《不得不爱》/audio.mp3', 
          cover: clientBaseUrl + '/audio/【AI心夏】《不得不爱》/cover.jpg', 
          lrc: '',
          theme: '#ebd0c2'
        },
        {
          name: '生日快乐歌',
          artist: 'AI心夏',
          url: clientBaseUrl + '/audio/【AI心夏】生日快乐歌/audio.mp3', 
          cover: clientBaseUrl + '/audio/【AI心夏】生日快乐歌/cover.jpg', 
          lrc: '',
          theme: '#46718b'
        },
        {
          name: '有点甜',
          artist: 'AI香奈美&AI心夏',
          url: clientBaseUrl + '/audio/【AI香奈美&AI心夏】《有点甜》用心刻画最幸福的风格/audio.mp3', 
          cover: clientBaseUrl + '/audio/【AI香奈美&AI心夏】《有点甜》用心刻画最幸福的风格/cover.jpg', 
          lrc: '',
          theme: '#f9f0ff'
        }
      ]
    }
    player = new APlayer(options)
  }
})

onUnmounted(() => {
  if (player) {
    player.destroy()
  }
})
</script>

<style scoped>
.global-player-wrapper {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}

:deep(.aplayer) {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
</style>