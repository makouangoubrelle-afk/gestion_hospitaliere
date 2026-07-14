<template>
  <div class="min-h-screen">
    <nav v-if="isAuthenticated" class="bg-gradient-to-r from-teal-700 to-teal-900 text-white px-6 py-4 flex gap-4 flex-wrap shadow-md">
      <router-link to="/dashboard" class="font-semibold">SGHL</router-link>
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/patients">Patients</router-link>
      <button @click="logout" class="ml-auto underline">Déconnexion</button>
    </nav>
    <main class="p-6">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isAuthenticated = computed(() => !!localStorage.getItem('access_token'))

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}
</script>
