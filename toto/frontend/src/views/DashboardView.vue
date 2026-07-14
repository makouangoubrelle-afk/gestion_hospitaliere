<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Tableau de bord administratif</h1>
    <div v-if="kpis" class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div v-for="(value, label) in cards" :key="label" class="bg-white rounded-2xl p-6 shadow">
        <p class="text-slate-500">{{ label }}</p>
        <p class="text-3xl font-bold text-blue-700 mt-2">{{ value }}</p>
      </div>
    </div>
    <p v-else class="text-slate-500">Chargement des KPIs...</p>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '../api'

const kpis = ref(null)

const cards = computed(() => {
  if (!kpis.value) return {}
  return {
    'Patients actifs': kpis.value.patients_actifs,
    "Taux d'occupation": `${kpis.value.taux_occupation}%`,
    'Recettes du mois': `${kpis.value.recettes_mois} FCFA`,
    'Examens en attente': kpis.value.examens_en_attente,
    'Lits disponibles': kpis.value.lits_disponibles,
    'Consultations du jour': kpis.value.consultations_du_jour,
  }
})

onMounted(async () => {
  const { data } = await api.get('/dashboard/kpis')
  kpis.value = data
})
</script>
