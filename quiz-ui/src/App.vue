<script setup>
  import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container-fluid">
        <RouterLink to="/" class="navbar-brand">Quiz App</RouterLink>
        <div class="navbar-nav ms-auto">
          <RouterLink to="/" class="nav-link">Home</RouterLink>
          <RouterLink to="/admin/login" class="nav-link">Administration</RouterLink>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>

