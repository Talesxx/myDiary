<template>
  <div class="global-player-wrapper">
    <div id="global-player" ref="playerRef"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
// @ts-ignore
import APlayer from 'aplayer'
import 'aplayer/dist/APlayer.min.css'

const playerRef = ref<HTMLElement>()
let player: APlayer | null = null

onMounted(() => {
  if (playerRef.value) {
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
          url: '../../../music/audio/【AI心夏】《不得不爱》.mp3', 
          cover: '', 
          lrc: '',
          theme: '#ebd0c2'
        },
        {
          name: '生日快乐歌',
          artist: 'AI心夏',
          url: '../../../music/audio/【AI心夏】生日快乐歌.mp3', 
          cover: '', 
          lrc: '',
          theme: '#46718b'
        },
        {
          name: '有点甜',
          artist: 'AI香奈美&AI心夏',
          url: '../../../music/audio/【AI香奈美&AI心夏】《有点甜》用心刻画最幸福的风格~.mp3', 
          cover: '', 
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