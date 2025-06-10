<template>
  <div>
    <img
        :src="src"
        class="cursor-pointer max-w-xs rounded border"
        @click="show = true"
        :alt="alt || 'preview'"
        style="max-width: 150px; max-height: 150px; object-fit: contain;"
    />
    <vue-easy-lightbox
      :visible="show"
      :imgs="[fullSrc]"
      @hide="show = false"
    />
  </div>
</template>

<script>
import VueEasyLightbox from 'vue-easy-lightbox'

export default {
  name: 'ImagePreview',
  components: { VueEasyLightbox },
  props: {
    src: String,
    alt: String
  },
  data() {
    return {
      show: false
    }
  },
  computed: {
    fullSrc() {
        const path = this.src.startsWith('/') ? this.src : `/${this.src}`;
        return this.src.startsWith('http') ? this.src : `http://127.0.0.1:8000${path}`;
    }
  },
  mounted() {
  console.log('ImagePreview src:', this.src);
  }
}
</script>