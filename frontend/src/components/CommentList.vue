<template>
  <div :class="wrapperClass">
    <div v-if="!comments" class="mb-4 flex items-center space-x-2">
      <label class="text-sm font-medium">Сортировать по:</label>
      <select v-model="sortBy" class="p-1 border rounded">
        <option value="-created_at">Дате (новые)</option>
        <option value="created_at">Дате (старые)</option>
        <option value="user__name">Имени</option>
        <option value="user__email">Email</option>
      </select>
    </div>

    <div
        v-for="comment in sortedComments"
        :key="comment.id"
        :class="[
        'border rounded p-4',
        depth === 0 ? 'bg-white' : 'bg-gray-100 text-sm ml-4 border-l-4 border-gray-400'
        ]"
    >
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

      <div v-if="comment.replies?.length" class="mt-4 space-y-2">
        <CommentList :comments="comment.replies" :depth="depth + 1" />
      </div>
    </div>

    <div v-if="!comments" class="flex justify-between items-center mt-4">
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
  },
    depth: {
        type: Number,
        default: 0
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
    } else {
      this.localComments = this.comments;
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
      this.page++;
      this.fetchComments();
    },
    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.fetchComments();
      }
    }
  },
  computed: {
    wrapperClass() {
      return this.isReply
        ? 'ml-4 text-sm bg-gray-50 p-2 border-l-2 border-blue-300 rounded'
        : 'max-w-3xl mx-auto space-y-4';
    },
    sortedComments() {
      const comments = this.localComments.slice();

      if (this.sortBy === 'user__name') {
        return comments.sort((a, b) =>
          (a.user?.name || '').localeCompare(b.user?.name || '')
        );
      }

      if (this.sortBy === 'user__email') {
        return comments.sort((a, b) =>
          (a.user?.email || '').localeCompare(b.user?.email || '')
        );
      }

      if (this.sortBy === 'created_at') {
        return comments.sort((a, b) =>
          new Date(a.created_at) - new Date(b.created_at)
        );
      }

      if (this.sortBy === '-created_at') {
        return comments.sort((a, b) =>
          new Date(b.created_at) - new Date(a.created_at)
        );
      }

      return comments;
    }
  },
  watch: {
    sortBy() {
      this.page = 1;
      this.fetchComments();
    }
  },
  components: {
    ImagePreview,
    CommentList: () => import('./CommentList.vue')
  }
};
</script>
