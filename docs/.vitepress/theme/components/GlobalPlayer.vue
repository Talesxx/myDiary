<template>
  <div class="global-player-wrapper">
    <div id="global-player" ref="playerRef"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import 'aplayer/dist/APlayer.min.css'

// 获取当前页面的baseURL路径，用于拼接音频地址
// @ts-ignore
const BaseURL = import.meta.env.BASE_URL;
const playerRef = ref<HTMLElement>()
let player: any | null = null

// 异步加载音乐配置
const loadMusicConfig = async () => {
  try {
    // 动态导入JSON配置文件
    // @ts-ignore
    const configModule = await import('../../../docsPublic/audio/music_config.json')
    return configModule.default || configModule
  } catch (error) {
    console.warn('无法加载音乐配置文件，使用默认配置')
    // 默认配置（保持原有配置作为后备）
    return []
  }
}

onMounted(async () => {
  if (playerRef.value) {
    // @ts-ignore 
    const APlayer = (await import('aplayer')).default
    
    // 加载音乐配置
    const audioList = await loadMusicConfig()
    
    // 在客户端环境中获取基础URL
    const clientBaseUrl = typeof window !== 'undefined' ? window.location.origin + BaseURL : BaseURL;
    
    // 为每个音频URL添加基础URL前缀
    const processedAudioList = audioList.map(item => ({
      ...item,
      url: clientBaseUrl + item.url,
      cover: clientBaseUrl + item.cover
    }))
    
    // 配置音乐播放器
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
      audio: processedAudioList
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