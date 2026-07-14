<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Patients</h1>
    <div class="bg-white rounded-2xl shadow overflow-x-auto">
      <table class="w-full text-left">
        <thead class="bg-indigo-50">
          <tr>
            <th class="p-4">ID</th>
            <th class="p-4">Nom</th>
            <th class="p-4">Email</th>
            <th class="p-4">Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in patients" :key="p.id" class="border-t">
            <td class="p-4">{{ p.patient_id }}</td>
            <td class="p-4">{{ p.first_name }} {{ p.last_name }}</td>
            <td class="p-4">{{ p.email }}</td>
            <td class="p-4">{{ p.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '../api'

const patients = ref([])

onMounted(async () => {
  const { data } = await api.get('/patients/')
  patients.value = data.items || data
})
</script>
