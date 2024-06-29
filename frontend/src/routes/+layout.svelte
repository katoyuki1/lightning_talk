<script>
  import "../app.css";
  import Header from '$lib/Header.svelte';
  import Footer from '$lib/Footer.svelte';
  import { isAuthenticated } from '../stores/auth';

  // Check for the token in local storage when the layout is loaded, but only in the browser
  if (typeof window !== 'undefined' && localStorage.getItem('authToken')) {
    isAuthenticated.set(true);
  }
</script>

<main class="bg-gray-100 min-h-screen">
  <Header />
  <slot />
  <Footer />
</main>