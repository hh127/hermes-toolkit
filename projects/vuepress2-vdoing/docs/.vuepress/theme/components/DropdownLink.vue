<template>
  <div class="dropdown-wrapper" :class="{ open }">
    <button
      class="dropdown-title"
      @click="toggle"
    >
      <span class="title">{{ item.text }}</span>
      <span class="arrow" :class="open ? 'down' : 'right'" />
    </button>

    <DropdownTransition>
      <ul class="nav-dropdown" v-show="open">
        <li
          class="dropdown-item"
          v-for="(child, index) in item.items"
          :key="index"
        >
          <h4 v-if="child.type === 'links'">{{ child.text }}</h4>
          <ul v-if="child.type === 'links'" class="dropdown-subitem">
            <li v-for="(grandchild, idx) in child.items" :key="idx">
              <RouterLink
                v-if="grandchild.link"
                :to="grandchild.link"
                class="nav-link"
                :class="{ active: isChildActive(grandchild) }"
              >{{ grandchild.text }}</RouterLink>
              <a
                v-else
                :href="grandchild.link"
                class="nav-link external"
                target="_blank"
                rel="noopener noreferrer"
              >{{ grandchild.text }}</a>
            </li>
          </ul>
          <RouterLink
            v-else-if="child.link"
            :to="child.link"
            class="nav-link"
            :class="{ active: isChildActive(child) }"
          >{{ child.text }}</RouterLink>
        </li>
      </ul>
    </DropdownTransition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vuepress/client'
import DropdownTransition from './DropdownTransition.vue'

const props = defineProps<{
  item: any
}>()

const route = useRoute()
const open = ref(false)

const toggle = () => {
  open.value = !open.value
}

const isChildActive = (child: any) => {
  if (child.link) {
    return route.path === child.link
  }
  return false
}
</script>

<style lang="scss">
.dropdown-wrapper {
  cursor: pointer;

  .dropdown-title {
    display: block;
    padding: 0 1.5rem;
    font-size: inherit;
    font-weight: 500;
    color: var(--textColor);
    background: transparent;
    border: none;
    width: 100%;
    text-align: left;
    cursor: pointer;
    outline: none;

    &:hover {
      color: var(--accentColor);
    }

    .arrow {
      display: inline-block;
      width: 0;
      height: 0;
      border: 5px solid transparent;
      position: relative;
      margin-left: 0.5rem;

      &.right {
        border-left-color: var(--textColor);
        left: 2px;
      }

      &.down {
        border-top-color: var(--textColor);
        top: 2px;
      }
    }
  }

  .nav-dropdown {
    padding: 0.5rem 0;
    margin: 0;
    list-style-type: none;

    .dropdown-item {
      h4 {
        margin: 0;
        padding: 0.5rem 1.5rem 0.2rem;
        font-size: 0.85em;
        color: var(--textColor);
        opacity: 0.6;
      }

      .dropdown-subitem {
        padding: 0;
        margin: 0;
        list-style-type: none;
      }

      .nav-link {
        display: block;
        padding: 0.3rem 1.5rem 0.3rem 2rem;
        font-size: 0.9em;
        color: var(--textColor);
        text-decoration: none;

        &:hover,
        &.active {
          color: var(--accentColor);
        }

        &.external::after {
          content: '↗';
          margin-left: 0.3rem;
          font-size: 0.7em;
        }
      }
    }
  }

  &.open {
    .dropdown-title {
      color: var(--accentColor);
    }
  }
}
</style>
