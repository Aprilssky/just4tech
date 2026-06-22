<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Personal Income Tax Calculator</h2>
      <p class="text-slate-600 dark:text-slate-400 mt-1">Calculate Chinese individual income tax (2025 brackets, salary income).</p>
    </div>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Monthly Pre-Tax Salary (CNY)</label>
        <input type="number" v-model.number="salary" min="0" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none" placeholder="e.g. 15000">
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Social Insurance & Housing Fund (monthly, CNY)</label>
        <input type="number" v-model.number="insurance" min="0" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none" placeholder="e.g. 2000">
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Special Deductions (monthly, CNY)</label>
        <input type="number" v-model.number="deductions" min="0" class="w-full px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500 outline-none" placeholder="e.g. 1000">
      </div>

      <div v-if="result" class="space-y-3">
        <h3 class="text-lg font-semibold text-slate-800 dark:text-slate-200">Tax Breakdown</h3>

        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <div class="p-4 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-center">
            <div class="text-xs text-amber-600 dark:text-amber-400 mb-1">Taxable Income</div>
            <div class="text-lg font-bold text-slate-900 dark:text-white">{{ formatMoney(result.taxableIncome) }}</div>
          </div>
          <div class="p-4 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-center">
            <div class="text-xs text-amber-600 dark:text-amber-400 mb-1">Monthly Tax</div>
            <div class="text-lg font-bold text-slate-900 dark:text-white">{{ formatMoney(result.monthlyTax) }}</div>
          </div>
          <div class="p-4 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-center">
            <div class="text-xs text-amber-600 dark:text-amber-400 mb-1">Net Income</div>
            <div class="text-lg font-bold text-slate-900 dark:text-white">{{ formatMoney(result.netIncome) }}</div>
          </div>
        </div>

        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-sm space-y-2">
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Pre-tax Salary</span>
            <span class="font-mono text-slate-900 dark:text-white">{{ formatMoney(salary) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Monthly Deduction (5,000)</span>
            <span class="font-mono text-slate-900 dark:text-white">-5,000</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Social Insurance</span>
            <span class="font-mono text-slate-900 dark:text-white">-{{ formatMoney(insurance) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Special Deductions</span>
            <span class="font-mono text-slate-900 dark:text-white">-{{ formatMoney(deductions) }}</span>
          </div>
          <hr class="border-slate-200 dark:border-slate-700">
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Taxable Income</span>
            <span class="font-mono font-semibold text-slate-900 dark:text-white">{{ formatMoney(result.taxableIncome) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Applicable Rate</span>
            <span class="font-mono text-slate-900 dark:text-white">{{ result.rate }}%</span>
          </div>
          <div v-if="result.quickDeduction > 0" class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Quick Deduction</span>
            <span class="font-mono text-slate-900 dark:text-white">{{ formatMoney(result.quickDeduction) }}</span>
          </div>
          <hr class="border-slate-200 dark:border-slate-700">
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Monthly Tax Payable</span>
            <span class="font-mono font-bold text-red-600 dark:text-red-400">{{ formatMoney(result.monthlyTax) }}</span>
          </div>
        </div>

        <div class="p-4 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-center">
          <div class="text-xs text-emerald-600 dark:text-emerald-400 mb-1">Net Monthly Income (after tax & insurance)</div>
          <div class="text-2xl font-bold text-slate-900 dark:text-white">{{ formatMoney(result.netIncome) }}</div>
        </div>

        <div class="p-4 rounded-lg bg-slate-50 dark:bg-slate-800 text-sm">
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Annual Tax</span>
            <span class="font-mono text-slate-900 dark:text-white">{{ formatMoney(result.monthlyTax * 12) }}</span>
          </div>
          <div class="flex justify-between mt-1">
            <span class="text-slate-500 dark:text-slate-400">Effective Tax Rate</span>
            <span class="font-mono text-slate-900 dark:text-white">{{ result.effectiveRate }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const salary = ref(15000)
const insurance = ref(2000)
const deductions = ref(1000)

// Chinese 2025 tax brackets (annual taxable income)
const brackets = [
  { min: 0, max: 36000, rate: 0.03, quickDeduction: 0 },
  { min: 36000, max: 144000, rate: 0.10, quickDeduction: 2520 },
  { min: 144000, max: 300000, rate: 0.20, quickDeduction: 16920 },
  { min: 300000, max: 420000, rate: 0.25, quickDeduction: 31920 },
  { min: 420000, max: 660000, rate: 0.30, quickDeduction: 52920 },
  { min: 660000, max: 960000, rate: 0.35, quickDeduction: 85920 },
  { min: 960000, max: Infinity, rate: 0.45, quickDeduction: 181920 },
]

const result = computed(() => {
  const monthlyDeduction = 5000
  const annualSalary = salary.value * 12
  const annualInsurance = insurance.value * 12
  const annualDeductions = deductions.value * 12
  const annualTaxable = Math.max(0, annualSalary - monthlyDeduction * 12 - annualInsurance - annualDeductions)

  let annualTax = 0
  let rate = 0
  let quickDeduction = 0

  for (const b of brackets) {
    if (annualTaxable > b.min && annualTaxable <= b.max) {
      annualTax = annualTaxable * b.rate - b.quickDeduction
      rate = b.rate * 100
      quickDeduction = b.quickDeduction
      break
    }
  }

  const monthlyTax = Math.max(0, annualTax / 12)
  const netIncome = salary.value - insurance.value - monthlyTax
  const effectiveRate = salary.value > 0 ? ((annualTax / annualSalary) * 100).toFixed(1) : '0.0'

  return {
    taxableIncome: Math.round(annualTaxable / 12),
    monthlyTax: Math.round(monthlyTax),
    netIncome: Math.round(netIncome),
    rate,
    quickDeduction,
    effectiveRate,
  }
})

function formatMoney(val) {
  return val.toLocaleString('en-US')
}
</script>
