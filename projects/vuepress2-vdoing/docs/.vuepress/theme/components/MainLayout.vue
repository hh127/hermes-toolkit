<template>
  <div class="main-layout">
    <div class="main-left">
      <slot name="mainLeft" />
    </div>
    <div class="main-right">
      <slot name="mainRight" />
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style lang="scss">
.main-layout {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2.5rem;
  display: flex;
  gap: 1.5rem;

  .main-left {
    flex: 1;
    min-width: 0;
  }

  .main-right {
    width: 280px;
    flex-shrink: 0;
  }
}

@media (max-width: 959px) {
  .main-layout {
    padding: 0 1.5rem;

    .main-right {
      display: none;
    }
  }
}

@media (max-width: 719px) {
  .main-layout {
    padding: 0 1rem;
  }
}
</style>
