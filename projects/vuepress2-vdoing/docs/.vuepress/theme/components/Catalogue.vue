<template>
  <div class="catalogue card-box">
    <h4 class="title">{{ title }}</h4>
    <div class="catalogue-list">
      <RouterLink
        :to="item.link"
        class="catalogue-item"
        v-for="(item, index) in items"
        :key="index"
      >
        <img
          v-if="item.img"
          :src="item.img"
          class="img"
        />
        <div class="info">
          <span class="name">{{ item.name }}</span>
          <span class="desc" v-if="item.desc">{{ item.desc }}</span>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePageFrontmatter } from 'vuepress/client'

const frontmatter = usePageFrontmatter()

const title = frontmatter.value.title || '目录'

const items = (frontmatter.value as any).catalogue || []
</script>

<style lang="scss">
.catalogue {
  padding: 1.5rem;

  .title {
    margin: 0 0 1rem;
    font-size: 1.1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--accentColor);
  }

  .catalogue-list {
    .catalogue-item {
      display: flex;
      align-items: center;
      padding: 0.8rem 0;
      border-bottom: 1px dashed var(--borderColor);
      text-decoration: none;
      color: var(--textColor);
      transition: all 0.2s;

      &:hover {
        color: var(--accentColor);
        padding-left: 0.5rem;
      }

      &:last-child {
        border-bottom: none;
      }

      .img {
        width: 50px;
        height: 50px;
        border-radius: 5px;
        margin-right: 1rem;
        object-fit: cover;
      }

      .info {
        flex: 1;

        .name {
          display: block;
          font-size: 1rem;
          font-weight: 500;
        }

        .desc {
          display: block;
          font-size: 0.85rem;
          color: var(--textColor);
          opacity: 0.7;
          margin-top: 0.3rem;
        }
      }
    }
  }
}
</style>
