<template>
  <div class="blogger-bar" v-if="blogger">
    <div class="blogger-avatar">
      <img :src="blogger.avatar" :alt="blogger.name" />
    </div>
    <div class="blogger-name">{{ blogger.name }}</div>
    <div class="blogger-slogan" v-if="blogger.slogan">{{ blogger.slogan }}</div>
    <div class="blogger-social" v-if="socialIcons.length">
      <a
        v-for="item in socialIcons"
        :key="item.link"
        :href="item.link"
        :title="item.title"
        target="_blank"
        rel="noopener noreferrer"
      >
        <span :class="['iconfont', item.iconClass]"></span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useThemeData } from '../composables'

const themeData = useThemeData()

const blogger = computed(() => themeData.value.blogger)
const socialIcons = computed(() => themeData.value.social?.icons || [])
</script>

<style lang="scss" scoped>
.blogger-bar {
  text-align: center;
  padding: 1rem 0;
  border-bottom: 1px solid var(--c-border);
  margin-bottom: 0.5rem;

  .blogger-avatar {
    width: 80px;
    height: 80px;
    margin: 0 auto 0.5rem;
    border-radius: 50%;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .blogger-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--c-text);
  }

  .blogger-slogan {
    font-size: 0.85rem;
    color: var(--c-text-lightest);
    margin-top: 0.25rem;
  }

  .blogger-social {
    margin-top: 0.75rem;

    a {
      display: inline-block;
      margin: 0 0.3rem;
      color: var(--c-text-lighter);
      font-size: 1.2rem;

      &:hover {
        color: var(--c-brand);
      }
    }
  }
}
</style>
