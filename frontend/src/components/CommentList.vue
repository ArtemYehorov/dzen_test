<template>
  <div class="max-w-3xl mx-auto space-y-4">
    <div v-for="comment in displayComments" :key="comment.id" class="bg-white border rounded p-4">
      <p class="text-sm text-gray-600">
        <strong>{{ comment.user.name }}</strong>
        <span class="text-gray-400">({{ comment.user.email }})</span>
        <br />
        <span class="text-xs">{{ formatDate(comment.created_at) }}</span>
      </p>
      <div class="mt-2" v-html="comment.text"></div>

      <div v-if="comment.image" class="mt-2">
        <img :src="`http://127.0.0.1:8000${comment.image}`" alt="картинка" class="max-w-xs rounded border" />
      </div>

      <div v-if="comment.file" class="mt-2">
        <a :href="`http://127.0.0.1:8000${comment.file}`" target="_blank" class="text-blue-600 underline">
          📎 Открыть файл
        </a>
      </div>

      <div v-if="comment.replies.length" class="mt-4 pl-4 border-l-2 border-gray-300 space-y-2">
        <CommentList :comments="comment.replies" />
      </div>
    </div>
  </div>
</template>

<script>
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
      loaded: false,
      localComments: []
    };
  },
  async created() {
    if (!this.comments) {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/comments/');
        this.localComments = response.data.results;
        this.loaded = true;
      } catch (err) {
        console.error('Ошибка загрузки комментариев', err);
      }
    }
  },
  methods: {
    formatDate(dateStr) {
      const d = new Date(dateStr);
      return d.toLocaleString();
    }
  },
  components: {
    CommentList: () => import('./CommentList.vue')
  },
  computed: {
    displayComments() {
        return this.comments || this.localComments || [];
  }
}
};
</script>