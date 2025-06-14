<template>
  <form @submit.prevent="submitComment" class="max-w-xl mx-auto bg-white p-4 rounded shadow space-y-4">
    <div>
      <input v-model="form.name" type="text" placeholder="Ваше имя" class="w-full border p-2 rounded" required />
    </div>
    <div>
      <input v-model="form.email" type="email" placeholder="Email" class="w-full border p-2 rounded" required />
    </div>
    <div>
      <input v-model="form.home_page" type="url" placeholder="Домашняя страница (опц.)" class="w-full border p-2 rounded" />
    </div>

    <div>
      <label class="block text-sm font-medium mb-1">Ответить на:</label>
      <select v-model="form.parent" class="w-full border p-2 rounded">
        <option :value="null">Новый заглавный комментарий</option>
        <option v-for="comment in topLevelComments" :key="comment.id" :value="comment.id">
          {{ comment.user.name }} — {{ comment.text.slice(0, 50) }}...
        </option>
      </select>
    </div>

    <div>
      <textarea v-model="form.text" placeholder="Комментарий..." rows="4" class="w-full border p-2 rounded" required></textarea>
    </div>

    <div class="border p-2 rounded bg-white text-black">
      <h3 class="font-semibold mb-1">Предпросмотр:</h3>
      <div v-html="sanitizedPreview"></div>
    </div>

    <div class="flex gap-2">
      <input type="file" @change="handleFileUpload" accept=".txt" />
      <input type="file" @change="handleImageUpload" accept="image/*" />
    </div>

    <div class="flex items-center gap-4">
      <img :src="captchaImageUrl" alt="CAPTCHA" class="cursor-pointer h-12" @click="loadCaptcha" />
      <input type="text" v-model="captchaInput" placeholder="Введите CAPTCHA" class="border p-2 rounded w-full" required />
    </div>

    <div class="flex gap-2">
      <button type="button" @click="insertTag('i')" class="bg-gray-200 px-2 py-1 rounded">[i]</button>
      <button type="button" @click="insertTag('strong')" class="bg-gray-200 px-2 py-1 rounded">[strong]</button>
      <button type="button" @click="insertTag('code')" class="bg-gray-200 px-2 py-1 rounded">[code]</button>
      <button type="button" @click="insertTag('a')" class="bg-gray-200 px-2 py-1 rounded">[a]</button>
    </div>

    <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Отправить</button>
  </form>
</template>

<script>
import axios from 'axios';
import DOMPurify from 'dompurify';

export default {
  data() {
    return {
      form: {
        name: '',
        email: '',
        home_page: '',
        text: '',
        parent: null,
        file: null,
        image: null
      },
      topLevelComments: [],
      captchaKey: '',
      captchaImageUrl: '',
      captchaInput: ''
    };
  },

  mounted() {
    this.loadCaptcha();
    this.loadTopLevelComments();
  },

  computed: {
    sanitizedPreview() {
      return DOMPurify.sanitize(this.form.text);
    }
  },

  methods: {
    insertTag(tag) {
      const open = `<${tag}>`;
      const close = `</${tag}>`;
      this.form.text += open + close;
    },

    handleFileUpload(event) {
      this.form.file = event.target.files[0];
    },

    handleImageUpload(event) {
      this.form.image = event.target.files[0];
    },

    async loadCaptcha() {
      try {
        const response = await axios.get('https://dzen-test-fjvl.onrender.com/api/comments/captcha/');
        this.captchaKey = response.data.captcha_key;
        this.captchaImageUrl = response.data.captcha_image_url;
      } catch (error) {
        console.error('Ошибка загрузки CAPTCHA:', error);
      }
    },

    async loadTopLevelComments() {
      try {
        const response = await axios.get('https://dzen-test-fjvl.onrender.com/api/comments/?page_size=1000');
        this.topLevelComments = response.data.results.filter(c => !c.parent);
      } catch (error) {
        console.error('Ошибка загрузки заглавных комментариев:', error);
      }
    },

    async submitComment() {
  try {
    const formData = new FormData();
    formData.append('name', this.form.name);
    formData.append('email', this.form.email);
    formData.append('home_page', this.form.home_page);
    formData.append('text', this.form.text);
    formData.append('captcha', this.captchaInput);
    formData.append('captcha_key', this.captchaKey);
    if (this.form.file) formData.append('file', this.form.file);
    if (this.form.image) formData.append('image', this.form.image);
    if (this.form.parent) formData.append('parent', this.form.parent);

    await axios.post('https://dzen-test-fjvl.onrender.com/api/comments/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    alert('Комментарий отправлен!');
    this.resetForm();
    this.loadCaptcha();
    this.loadTopLevelComments();

    // 🔥 Обновление списка через ref
    if (this.$refs.commentList) {
      this.$refs.commentList.fetchComments();
    }
  } catch (error) {
    alert('Ошибка при отправке: ' + (error.response?.data?.captcha || error.response?.data?.detail || error.message));
    this.loadCaptcha();
    console.error(error);
  }
},

    resetForm() {
      this.form = {
        name: '',
        email: '',
        home_page: '',
        text: '',
        parent: null,
        file: null,
        image: null
      };
      this.captchaInput = '';
    }
  }
};
</script>