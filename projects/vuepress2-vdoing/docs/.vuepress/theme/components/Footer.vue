<template>
  <div class="footer">
    <div class="footer-inner">
      <div class="copyright" v-if="footer.copyright">
        <span v-html="footer.copyright" />
      </div>
      <div class="powered-by">
        <span>Powered by <a href="https://v2.vuepress.vuejs.org/" target="_blank" rel="noopener noreferrer">VuePress 2.x</a></span>
        <span v-if="footer.theme">&nbsp;|&nbsp;{{ footer.theme }}</span>
      </div>
      <div class="备案信息" v-if="footer.beian">
        <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">{{ footer.beian }}</a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSiteData } from 'vuepress/client'

const site = useSiteData()

const footer = computed(() => {
  return site.value?.themeConfig?.footer || {}
})
</script>

<style lang="scss">
.footer {
  padding: 2.5rem;
  text-align: center;
  font-size: 0.85rem;
  color: var(--textColor);
  opacity: 0.7;

  .footer-inner {
    max-width: 1200px;
    margin: 0 auto;
    border-top: 1px solid var(--borderColor);
    padding-top: 1.5rem;

    .copyright {
      margin-bottom: 0.5rem;
    }

    .powered-by {
      margin-bottom: 0.5rem;

      a {
        color: var(--accentColor);
        text-decoration: none;

        &:hover {
          color: var(--accentColorDark);
        }
      }
    }

    .备案信息 {
      a {
        color: var(--textColor);
        text-decoration: none;

        &:hover {
          color: var(--accentColor);
        }
      }
    }
  }
}
</style>
