<template>
  <form @submit.prevent="submitComment" class="max-w-xl mx-auto bg-white p-4 rounded shadow space-y-4">
    <div>
      <input v-model="form.user.name" type="text" placeholder="Ваше имя" class="w-full border p-2 rounded" required />
    </div>
    <div>
      <input v-model="form.user.email" type="email" placeholder="Email" class="w-full border p-2 rounded" required />
    </div>
    <div>
      <input v-model="form.user.home_page" type="url" placeholder="Домашняя страница (опц.)" class="w-full border p-2 rounded" />
    </div>
    <div>
      <textarea v-model="form.text" placeholder="Комментарий..." rows="4" class="w-full border p-2 rounded" required></textarea>
    </div>
    <div class="flex gap-2">
      <input type="file" @change="handleFileUpload" accept=".txt" />
      <input type="file" @change="handleImageUpload" accept="image/*" />
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

export default {
  data() {
    return {
      form: {
        user: {
          name: '',
          email: '',
          home_page: '',
        },
        text: '',
        parent: null,
        file: null,
        image: null,
      }
    };
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
    async submitComment() {
      try {
        const formData = new FormData();
        formData.append('user.name', this.form.user.name);
        formData.append('user.email', this.form.user.email);
        formData.append('user.home_page', this.form.user.home_page);
        formData.append('text', this.form.text);
        if (this.form.file) formData.append('file', this.form.file);
        if (this.form.image) formData.append('image', this.form.image);
        if (this.form.parent) formData.append('parent', this.form.parent);

        const response = await axios.post('http://127.0.0.1:8000/api/comments/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        alert('Комментарий отправлен!');
        this.form.text = '';
        this.form.file = null;
        this.form.image = null;
      } catch (error) {
        alert('Ошибка при отправке: ' + error.message);
        console.error(error);
      }
    }
  }
};
</script>