<script>
  import "../app.css";
  import Header from '$lib/Header.svelte';
  import Footer from '$lib/Footer.svelte';
</script>

<main class="bg-gray-100 min-h-screen">
  <Header />
  <slot />
  <Footer />
</main>