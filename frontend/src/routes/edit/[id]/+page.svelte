<script lang="ts">
  import { onMount } from 'svelte';
  import axios from 'axios';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  let title = '';
  let description = '';
  let file: File | null = null;
  let videoUrl = '';

  const videoId = $page.params.id;

  onMount(async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/videos/${videoId}`);
      title = response.data.title;
      description = response.data.description;
      videoUrl = response.data.video; // URLとしてのビデオファイルのパス
    } catch (e) {
      console.error('Video not found', e);
    }
  });

  async function handleSubmit(event: Event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    if (file) {
      formData.append('video', file);
    }

    try {
      await axios.put(`http://127.0.0.1:8000/api/videos/${videoId}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      goto('/index'); // 成功したら一覧ページに戻る
    } catch (error) {
      console.error('Update failed', error);
    }
  }

  async function deleteVideo() {
    if (!confirm('本当に削除しますか？')) return;
    try {
      await axios.delete(`http://127.0.0.1:8000/api/videos/${videoId}`);
      goto('/index'); // Successfully deleted, redirect to the list
    } catch (error) {
      console.error('Failed to delete the video', error);
    }
  }
</script>

<main>
  <h1>動画を編集</h1>
  <form on:submit={handleSubmit}>
    <div>
      <label for="title">タイトル:</label>
      <input id="title" type="text" bind:value={title} required>
    </div>
    <div>
      <label for="description">説明:</label>
      <textarea id="description" bind:value={description} required></textarea>
    </div>
    <div>
      <label for="file">ビデオファイル:</label>
      <input id="file" type="file" accept="video/*" on:change={e => file = e.target.files[0]}>
    </div>
    {#if videoUrl}
      <p>現在のビデオ:</p>
      <video width="320" height="240" controls>
        <source src={videoUrl} type="video/mp4">
        Your browser does not support the video tag.
      </video>
    {/if}
    <button type="submit">更新</button>
  </form>
  <form on:submit={handleSubmit}>
    <!-- Form fields -->
    <button type="button" on:click={deleteVideo}>削除</button>
  </form>
  <button on:click={() => goto('/index')}>一覧に戻る</button>
</main>
