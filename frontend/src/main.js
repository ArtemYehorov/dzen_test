import axios from 'axios';
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

createApp(App).mount('#app')

axios.defaults.baseURL = 'https://dzen-test-fjvl.onrender.com';

