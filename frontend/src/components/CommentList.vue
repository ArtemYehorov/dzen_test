<template>
  <div class="max-w-3xl mx-auto space-y-4">
    <div class="mb-4 flex items-center space-x-2">
      <label class="text-sm font-medium">Сортировать по:</label>
      <select v-model="sortBy" class="p-1 border rounded">
        <option value="-created_at">Дате (новые)</option>
        <option value="created_at">Дате (старые)</option>
        <option value="user.name">Имени</option>
        <option value="user.email">Email</option>
      </select>
    </div>

    <div v-for="comment in sortedComments" :key="comment.id" class="bg-white border rounded p-4">
      <p class="text-sm text-gray-600">
        <strong>{{ comment.user.name }}</strong>
        <span class="text-gray-400">({{ comment.user.email }})</span><br />
        <span class="text-xs">{{ formatDate(comment.created_at) }}</span>
      </p>
      <div class="mt-2" v-html="comment.text"></div>

      <div v-if="comment.image" class="mt-2">
        <ImagePreview :src="comment.image" />
      </div>

      <div v-if="comment.file" class="mt-2">
        <a :href="`https://dzen-test-fjvl.onrender.com${comment.file}`" target="_blank" class="text-blue-600 underline">
          📎 Открыть файл
        </a>
      </div>

      <div v-if="comment.replies?.length" class="mt-4 pl-4 border-l-2 border-gray-300 space-y-2">
        <CommentList :comments="comment.replies" />
      </div>
    </div>

    <div class="flex justify-between items-center mt-4">
      <button @click="prevPage" :disabled="page <= 1" class="px-3 py-1 border rounded">← Назад</button>
      <span>Страница {{ page }}</span>
      <button @click="nextPage" :disabled="!hasNext" class="px-3 py-1 border rounded">Вперёд →</button>
    </div>
  </div>
</template>

<script>
import ImagePreview from './ImagePreview.vue';
import axios from 'axios';

export default {
  name: 'CommentList',
  props: {
    comments: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      localComments: [],
      page: 1,
      sortBy: '-created_at',
      hasNext: false
    };
  },
  mounted() {
    if (!this.comments) {
      this.fetchComments();
    }
  },
  watch: {
    sortBy() {
      this.page = 1;
      this.fetchComments();
    },
    page() {
      this.fetchComments();
    }
  },
  methods: {
    formatDate(dateStr) {
      const d = new Date(dateStr);
      return d.toLocaleString();
    },
    async fetchComments() {
      try {
        const res = await axios.get('https://dzen-test-fjvl.onrender.com/api/comments/', {
          params: {
            page: this.page,
            ordering: this.sortBy
          }
        });
        this.localComments = res.data.results;
        this.hasNext = !!res.data.next;
      } catch (err) {
        console.error('Ошибка загрузки комментариев', err);
      }
    },
    nextPage() {
      if (this.page < 100) { // защита от зацикливания
        this.page++;
      }
    },
    prevPage() {
      if (this.page > 1) {
        this.page--;
      }
    }
  },
  components: {
    ImagePreview
  }
};
</script>