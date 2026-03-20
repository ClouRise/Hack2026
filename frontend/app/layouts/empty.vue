<template>
  <main class="bg-test-page min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-lg w-[440px] card-test-shadows">
      <div class="p-6">
        <slot />
      </div>
    </div>
  </main>
</template>

<style lang="css" scoped>
.card-test-shadows{
  box-shadow: 
    22px 22px 30px 0px rgba(7, 98, 104, 0.8),
    -22px -22px 30px 0px rgba(29, 208, 103, 0.3)
}
</style>