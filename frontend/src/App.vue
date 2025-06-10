<template>
  <main class="p-8 bg-gray-100 min-h-screen space-y-6">
    <h1 class="text-2xl font-bold">Добавить комментарий</h1>
    <CommentForm />

    <h2 class="text-xl font-semibold mt-8">Комментарии</h2>
    <CommentList />
  </main>
</template>

<script>
import CommentForm from './components/CommentForm.vue'
import CommentList from './components/CommentList.vue'

export default {
  components: {
    CommentForm,
    CommentList
  }
}
</script>