<template>
  <div class="max-w-xl mx-auto p-6 bg-white rounded-2xl shadow-lg space-y-6">
    <h1 class="text-2xl font-bold text-center">💬 Комментарии</h1>
    
    <form @submit.prevent="addComment" class="space-y-4">
      <input
        v-model="name"
        type="text"
        placeholder="Ваше имя"
        class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
      <textarea
        v-model="message"
        placeholder="Ваш комментарий"
        class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        rows="4"
        required
      ></textarea>
      <button
        type="submit"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition duration-200"
      >
        Отправить
      </button>
    </form>

    <div v-if="comments.length" class="space-y-4">
      <h2 class="text-xl font-semibold border-b pb-1">📝 Все комментарии</h2>
      <div v-for="(comment, index) in comments" :key="index" class="bg-gray-100 p-4 rounded-lg">
        <p class="font-bold">{{ comment.name }}</p>
        <p class="text-gray-700">{{ comment.message }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const message = ref('')
const comments = ref([])

function addComment() {
  comments.value.push({
    name: name.value,
    message: message.value,
  })
  name.value = ''
  message.value = ''
}
</script>