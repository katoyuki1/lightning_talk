<script lang="ts">
  import axios from 'axios';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  interface Video {
    title: string;
    description: string;
    video: string; // URLとしてのビデオファイルのパス
    created_at?: string; // 日付は文字列として扱う
  }

  let videos: Video[] = [];

  onMount(async () => {
    const response = await axios.get('http://127.0.0.1:8000/api/videos/');
    videos = response.data;
  });

  async function deleteVideo(id: number) {
    if (!confirm('本当に削除しますか？')) return;
    try {
      await axios.delete(`http://127.0.0.1:8000/api/videos/${id}`);
      videos = videos.filter(video => video.id !== id); // Remove video from list
    } catch (error) {
      console.error('Failed to delete the video', error);
    }
  }
</script>

<main class="bg-gray-100 min-h-screen">
  <!-- ヘッダー -->
  <header class="bg-blue-600 text-white p-4 shadow-md">
    <h1 class="text-3xl font-bold">Talk Advisor</h1>
    <div>
      <button class="mr-4 bg-white text-blue-600 px-4 py-2 rounded" on:click={() => openModal('logout')}>ログアウト</button>
  </div>
  </header>
   <section class="py-12">
    <div class="container mx-auto">
  <h1>ビデオ一覧</h1>
  <button on:click={() => goto('/upload')}>新規作成</button>
  <ul>
    {#each videos as video}
      <li>{video.title} - {video.description}</li>
			<video width="320" height="240" controls>
        <source src="{video.video}" type="video/mp4">
        Your browser does not support the video tag.
      </video>
      <button on:click={() => goto(`/edit/${video.id}`)}>編集</button>
      <button on:click={() => deleteVideo(video.id)}>削除</button>
    {/each}
  </ul>
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
    .video-card {
    transition: transform 0.3s;
  }

  .video-card:hover {
    transform: scale(1.05);
  }
  main {
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }
</style>