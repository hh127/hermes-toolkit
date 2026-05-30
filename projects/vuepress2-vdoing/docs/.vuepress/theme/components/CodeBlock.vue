<template>
  <div class="code-block-wrapper">
    <div class="code-block">
      <div class="code-block-header">
        <span class="code-block-title" v-if="title">{{ title }}</span>
        <span class="code-block-lang" v-if="lang">{{ lang }}</span>
      </div>
      <div class="code-block-content">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  lang?: string
}>(), {
  title: '',
  lang: ''
})
</script>

<style lang="scss">
.code-block-wrapper {
  margin: 1rem 0;

  .code-block {
    background: var(--codeBgColor, #282c34);
    border-radius: 6px;
    overflow: hidden;

    .code-block-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 1rem;
      background: rgba(0, 0, 0, 0.2);

      .code-block-title {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
      }

      .code-block-lang {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
      }
    }

    .code-block-content {
      padding: 1rem;
      overflow-x: auto;

      pre {
        margin: 0;
        padding: 0;
        background: transparent;

        code {
          font-family: 'Fira Code', 'Source Code Pro', Consolas, Monaco, Menlo, 'Courier New', monospace;
          font-size: 0.85rem;
          line-height: 1.6;
          color: #fff;
        }
      }
    }
  }
}
</style>
