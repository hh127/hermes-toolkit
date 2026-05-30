<template>
  <div class="blogger-bar card-box">
    <div class="blogger-info" v-if="blogger">
      <img
        class="avatar"
        :src="blogger.avatar"
        :alt="blogger.name"
      />
      <div class="info">
        <h3 class="name">{{ blogger.name }}</h3>
        <p class="slogan" v-if="blogger.slogan">{{ blogger.slogan }}</p>
        <div class="social" v-if="blogger.social">
          <a
            :href="item.link"
            :title="item.title"
            :class="['iconfont', item.iconClass]"
            v-for="(item, index) in blogger.social.icons"
            :key="index"
            target="_blank"
            rel="noopener noreferrer"
          />
        </div>
      </div>
    </div>
    <div class="data-info" v-if="blogger">
      <div class="data-item">
        <span class="count">{{ postCount }}</span>
        <span class="label">文章</span>
      </div>
      <div class="data-item">
        <span class="count">{{ categoriesCount }}</span>
        <span class="label">分类</span>
      </div>
      <div class="data-item">
        <span class="count">{{ tagsCount }}</span>
        <span class="label">标签</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSiteData } from 'vuepress/client'
import { usePosts } from '../composables/usePosts'

const site = useSiteData()

const blogger = computed(() => site.value?.themeConfig?.blogger)

// 使用文章数据 composable
const { postCount, categoriesCount, tagsCount } = usePosts()
</script>

<style lang="scss">
.blogger-bar {
  padding: 1.5rem;
  margin-bottom: 1rem;

  .blogger-info {
    display: flex;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--borderColor);

    .avatar {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      margin-right: 1rem;
      object-fit: cover;
    }

    .info {
      flex: 1;

      .name {
        margin: 0;
        font-size: 1.1rem;
      }

      .slogan {
        margin: 0.3rem 0 0;
        font-size: 0.85rem;
        color: var(--textColor);
        opacity: 0.7;
      }

      .social {
        margin-top: 0.5rem;

        a {
          display: inline-block;
          margin-right: 0.8rem;
          color: #777;
          font-size: 1.2rem;
          text-decoration: none;

          &:hover {
            color: var(--accentColor);
          }
        }
      }
    }
  }

  .data-info {
    display: flex;
    justify-content: space-around;
    padding-top: 1rem;

    .data-item {
      text-align: center;

      .count {
        display: block;
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--accentColor);
      }

      .label {
        display: block;
        font-size: 0.8rem;
        color: var(--textColor);
        opacity: 0.7;
        margin-top: 0.2rem;
      }
    }
  }
}
</style>
