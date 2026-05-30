<template>
  <span
    class="badge"
    :class="[type, vertical]"
    v-if="text"
  >{{ text }}</span>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  text?: string
  type?: string
  vertical?: string
}>(), {
  text: '',
  type: 'tip',
  vertical: ''
})
</script>

<style lang="scss">
.badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.1rem 0.5rem;
  border-radius: 0.75rem;
  line-height: 1;
  vertical-align: middle;
  margin-left: 0.3rem;

  &.tip {
    background-color: var(--accentColor);
    color: #fff;
  }

  &.warning {
    background-color: #e7c000;
    color: #fff;
  }

  &.danger {
    background-color: #cc0000;
    color: #fff;
  }

  &.top {
    vertical-align: top;
  }

  &.middle {
    vertical-align: middle;
  }
}
</style>
