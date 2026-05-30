<template>
  <header class="navbar">
    <button class="sidebar-button" @click="emit('toggle-sidebar')">
      <span class="menu-icon">☰</span>
    </button>

    <RouterLink to="/" class="navbar-brand">
      <img v-if="themeData.logo" :src="themeData.logo" class="navbar-logo" />
      <span>{{ site.title }}</span>
    </RouterLink>

    <nav class="navbar-links">
      <template v-for="item in nav" :key="item.link">
        <div v-if="item.items" class="nav-dropdown">
          <span class="nav-item dropdown-trigger">
            {{ item.text }}
            <span class="arrow">▾</span>
          </span>
          <ul class="dropdown-menu">
            <li v-for="subItem in item.items" :key="subItem.link">
              <RouterLink :to="subItem.link" class="dropdown-link">
                {{ subItem.text }}
              </RouterLink>
            </li>
          </ul>
        </div>
        <RouterLink v-else :to="item.link" class="nav-item">
          {{ item.text }}
        </RouterLink>
      </template>
    </nav>

    <div class="navbar-right">
      <SearchBox />
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSiteData } from 'vuepress/client'
import { useThemeData } from '../composables'
import SearchBox from './SearchBox.vue'

const emit = defineEmits<{
  'toggle-sidebar': []
}>()

const site = useSiteData()
const themeData = useThemeData()

const nav = computed(() => themeData.value.nav || [])
</script>

<style lang="scss" scoped>
.navbar {
  position: fixed;
  z-index: 20;
  top: 0;
  left: 0;
  right: 0;
  height: 3.6rem;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  background: var(--c-bg);
  border-bottom: 1px solid var(--c-border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);

  .navbar-brand {
    display: flex;
    align-items: center;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--c-text);
    text-decoration: none;
    margin-right: 2rem;

    &:hover {
      text-decoration: none;
    }
  }

  .navbar-logo {
    height: 1.8rem;
    margin-right: 0.5rem;
  }

  .navbar-links {
    display: flex;
    align-items: center;
    gap: 1.5rem;

    .nav-item {
      color: var(--c-text-lighter);
      font-size: 0.95rem;
      text-decoration: none;
      transition: color 0.2s;
      cursor: pointer;

      &:hover {
        color: var(--c-brand);
        text-decoration: none;
      }
    }

    .nav-dropdown {
      position: relative;

      .dropdown-trigger {
        display: flex;
        align-items: center;
        gap: 0.25rem;
      }

      .arrow {
        font-size: 0.7rem;
      }

      .dropdown-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        min-width: 150px;
        padding: 0.5rem 0;
        background: var(--c-bg);
        border: 1px solid var(--c-border);
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        list-style: none;
        margin: 0;

        .dropdown-link {
          display: block;
          padding: 0.4rem 1rem;
          color: var(--c-text-lighter);
          text-decoration: none;

          &:hover {
            color: var(--c-brand);
            background: var(--c-bg-lighter);
          }
        }
      }

      &:hover .dropdown-menu {
        display: block;
      }
    }
  }

  .navbar-right {
    margin-left: auto;
  }

  .sidebar-button {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    font-size: 1.2rem;
    color: var(--c-text);

    @media (max-width: 959px) {
      display: block;
    }
  }
}
</style>
