<template>
  <div class="max-w-3xl mx-auto space-y-4">
  <div class="mb-4">
  <label class="text-sm font-medium">Сортировать по: </label>
  <select v-model="sortBy" class="ml-2 p-1 border rounded">
    <option value="created_at">Дате</option>
    <option value="user.name">Имени</option>
    <option value="user.email">Email</option>
  </select>
</div>
    <div v-for="comment in displayComments" :key="comment.id" class="bg-white border rounded p-4">
      <p class="text-sm text-gray-600">
        <strong>{{ comment.user.name }}</strong>
        <span class="text-gray-400">({{ comment.user.email }})</span>
        <br />
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

      <div v-if="comment.replies.length" class="mt-4 pl-4 border-l-2 border-gray-300 space-y-2">
        <CommentList :comments="comment.replies" />
      </div>
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
      loaded: false,
      sortBy: 'created_at',
      localComments: []
    };
  },
  async created() {
    if (!this.comments) {
      try {
        const response = await axios.get('https://dzen-test-fjvl.onrender.com/api/comments/');
        this.localComments = response.data.results;
        this.loaded = true;
      } catch (err) {
        console.error('Ошибка загрузки комментариев', err);
      }
    }
  },
  methods: {
  extractField(obj, path) {
    return path.split('.').reduce((acc, key) => acc?.[key], obj);
  },
  formatDate(dateStr) {
    const d = new Date(dateStr);
    return d.toLocaleString();
  }
},
  components: {
    ImagePreview,
    CommentList: () => import('./CommentList.vue')
  },
    computed: {
        displayComments() {
    const list = this.comments || this.localComments || [];

    return list.slice().sort((a, b) => {
      let aValue = this.extractField(a, this.sortBy);
      let bValue = this.extractField(b, this.sortBy);

      aValue = (aValue || '').toString().toLowerCase();
      bValue = (bValue || '').toString().toLowerCase();

      return aValue.localeCompare(bValue);
    });
  }
}
};
</script>