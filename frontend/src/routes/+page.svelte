<script>
  import axios from 'axios';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { writable } from 'svelte/store';

  let faqs = [
    { question: "Talk Advisorとは何ですか？", answer: "Talk Advisorは自分のプレゼン音声・動画を投稿することで、AIから改善点を教えてもらえるアプリです。" },
    { question: "料金プランについて教えてください。", answer: "複数のプランがあります。詳細は下記をご覧ください。" },
    { question: "サポートはありますか？", answer: "はい、24時間対応のサポートがあります。" }
  ];

  let plans = [
    { title: "月額プラン", price: "¥500/月", features: ["基本機能", "24時間サポート"] },
    { title: "年間プラン", price: "¥5000/月", features: ["全機能", "プレミアムサポート"] },
    // { title: "プロプラン", price: "¥3,000/月", features: ["全機能", "専任サポート"] }
  ];
  let showModal = false;
  let modalType = '';
  let username = '';
  let email = '';
  let password = '';
  let password1 = '';
  let password2 = '';
  let message = writable('');


  function openModal(type) {
    modalType = type;
    showModal = true;
  }

  function closeModal() {
    showModal = false;
  }

  async function signup() {
      const payload = { email, password1, password2 };
      console.log("Sending payload:", payload);

      try {
        const response = await fetch('http://localhost:8000/auth/registration/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        console.log("Response data:", data);

        if (response.ok) {
          message.set('Registration successful. Check your email to confirm.');
        } else {
          message.set(`Error: ${JSON.stringify(data)}`);
        }
      } catch (error) {
        console.error("Fetch error:", error);
        message.set(`Fetch error: ${error}`);
      }
    }

  async function login() {
    const payload = { email, password };
    console.log("Sending payload:", payload);

    try {
      const response = await fetch('http://localhost:8000/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      console.log("Response data:", data);

      if (response.ok) {
        // トークンをローカルストレージに保存
        localStorage.setItem('authToken', data.key);
        console.log("Token saved to localStorage:", data.key); // 保存されたトークンを確認
        message.set('Login successful.');
        // indexページにリダイレクト
        goto('/index'); 
      } else {
        message.set(`Login failed: ${JSON.stringify(data)}`);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      message.set(`Fetch error: ${error}`);
    }
  }
</script>

<main class="bg-gray-100 min-h-screen">
  <!-- ヘッダー -->
  <header class="bg-blue-600 text-white p-4 shadow-md">
    <h1 class="text-3xl font-bold">Talk Advisor</h1>
    <div>
      <button class="mr-4 bg-white text-blue-600 px-4 py-2 rounded" on:click={() => openModal('login')}>ログイン</button>
      <button class="bg-white text-blue-600 px-4 py-2 rounded" on:click={() => openModal('signup')}>新規登録</button>
      <button class="mr-4 bg-white text-blue-600 px-4 py-2 rounded" on:click={async () => {
        await axios.post('http://127.0.0.1:8000/api/logout/');
        goto('/');
      }}>ログアウト</button>
    </div>
  </header>

  <!-- モーダル -->
  <!-- モーダル -->
  {#if showModal}
    <div class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full relative">
        <button class="absolute top-0 right-0 m-4 text-gray-600" on:click={closeModal}>✖️</button>
        {#if modalType === 'login'}
          <h2 class="text-2xl font-bold mb-4">ログイン</h2>
          <input type="email" bind:value={email} placeholder="Email" class="border p-2 mb-4 w-full" />
          <input type="password" bind:value={password} placeholder="Password" class="border p-2 mb-4 w-full" />
          <button class="bg-blue-600 text-white px-4 py-2 rounded w-full mb-4" on:click={login}>ログイン</button>
        {:else if modalType === 'signup'}
          <h2 class="text-2xl font-bold mb-4">新規登録</h2>
          <input type="email" bind:value={email} placeholder="Email" class="border p-2 mb-4 w-full" />
          <input type="password" bind:value={password1} placeholder="Password" class="border p-2 mb-4 w-full" />
          <input type="password" bind:value={password2} placeholder="Confirm Password" class="border p-2 mb-4 w-full" />
          <button class="bg-blue-600 text-white px-4 py-2 rounded w-full mb-4" on:click={signup}>登録する</button>
        {/if}
        <button class="bg-gray-600 text-white px-4 py-2 rounded w-full" on:click={closeModal}>とじる</button>
      </div>
    </div>
  {/if}

  <!-- ヘッダー画像欄 -->
  <section class="bg-cover bg-center h-64" style="background-image: url('https://via.placeholder.com/1500');">
    <div class="flex items-center justify-center h-full bg-black bg-opacity-50">
      <h2 class="text-4xl text-white">ようこそTalk Advisorへ</h2>
    </div>
  </section>

  <!-- プラン欄 -->
  <section class="py-12">
    <div class="container mx-auto">
      <h2 class="text-3xl font-bold text-center mb-8">プラン</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        {#each plans as plan}
          <div class="bg-white p-6 rounded-lg shadow-lg">
            <h3 class="text-xl font-bold mb-4">{plan.title}</h3>
            <p class="text-gray-700 mb-4">{plan.price}</p>
            <ul class="text-gray-600 mb-4">
              {#each plan.features as feature}
                <li>• {feature}</li>
              {/each}
            </ul>
            <button class="bg-blue-600 text-white px-4 py-2 rounded">申し込む</button>
          </div>
        {/each}
      </div>
      <div class="text-center mt-8">
        <button class="bg-green-600 text-white px-6 py-3 rounded-lg">入会手続きはこちら</button>
      </div>
    </div>
  </section>

  <!-- FAQセクション -->
  <section class="py-12 bg-gray-200">
    <div class="container mx-auto">
      <h2 class="text-3xl font-bold text-center mb-8">よくあるご質問</h2>
      <div class="space-y-4">
        {#each faqs as faq}
          <div class="bg-white p-4 rounded-lg shadow-lg">
            <h3 class="text-xl font-bold mb-2">{faq.question}</h3>
            <p class="text-gray-700">{faq.answer}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>
</main>
<main class="bg-gray-100 min-h-screen">
  <!-- 既存のコード -->

  <!-- フッター -->
  <footer class="bg-gray-800 text-white py-6 mt-12">
    <div class="container mx-auto text-center">
      <p>&copy; 2024 Talk Advisor. All rights reserved.</p>
    </div>
  </footer>
</main>

<style>
  main {
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }
</style>