<template>
  <div class="bg-test-page fixed inset-0 overflow-hidden">
    <div class="h-full overflow-y-auto">
      <div class="flex items-center justify-center p-4 min-h-full">
        <div class="bg-white rounded-lg w-[440px] card-test-shadows my-4">
          <div class="p-6">
            <slot />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="css" scoped>
/* .bg-test-page {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #144210;
  background-image: url('../assets/images/elements.svg');
  background-attachment: fixed;
  background-size: cover;
} */

.overflow-y-auto {
  overflow-y: auto;
  height: 100%;
}

.min-h-full {
  min-height: 100%;
}

.my-4 {
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>