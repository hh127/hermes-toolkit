<template>
  <div
    class="sidebar-group"
    :class="{ first, 'is-group': true, open }"
  >
    <p
      class="sidebar-heading"
      :class="{ open }"
      @click="$emit('toggle')"
    >
      <span>{{ item.title }}</span>
      <span
        class="arrow"
        :class="open ? 'down' : 'right'"
        v-if="collapsable"
      />
    </p>

    <DropdownTransition>
      <ul
        class="sidebar-group-items"
        ref="items"
        v-show="open"
      >
        <li v-for="(child, index) in item.children" :key="index">
          <SidebarLink :item="child" />
        </li>
      </ul>
    </DropdownTransition>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import DropdownTransition from './DropdownTransition.vue'
import SidebarLink from './SidebarLink.vue'

const props = withDefaults(defineProps<{
  item: any
  open?: boolean
  first?: boolean
  depth?: number
}>(), {
  open: false,
  first: false,
  depth: 0
})

defineEmits(['toggle'])

const collapsable = computed(() => {
  return props.item.collapsable !== false
})
</script>

<style lang="scss">
.sidebar-group {
  &:not(.first) {
    margin-top: 0.5rem;
  }

  .sidebar-heading {
    color: var(--textColor);
    font-size: 0.95em;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.35rem 1.5rem 0.35rem 1.25rem;
    margin: 0;
    width: 100%;
    box-sizing: border-box;

    &:hover {
      color: var(--accentColor);
    }

    &.open {
      color: var(--accentColor);
    }

    .arrow {
      display: inline-block;
      width: 0;
      height: 0;
      border: 6px solid transparent;
      position: relative;

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

  .sidebar-group-items {
    padding: 0;
    margin: 0;
    list-style-type: none;
    overflow: hidden;
    transition: height 0.1s ease-out;
  }
}
</style>
