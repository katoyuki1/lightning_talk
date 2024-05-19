<script lang="ts">
  import axios from 'axios';
  import { goto } from '$app/navigation';

  let title = '';
  let description = '';
  let file: File | null = null;

  async function handleSubmit(event: Event) {
    event.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('video', file);

    try {
      await axios.post('http://127.0.0.1:8000/api/videos/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      goto('/index'); // 成功したら一覧ページに戻る
    } catch (error) {
      console.error('Upload failed', error);
    }
  }
</script>

<main>
  <h1>動画をアップロード</h1>
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
      <input id="file" type="file" accept="video/*" on:change={e => file = e.target.files[0]} required>
    </div>
    <button type="submit">アップロード</button>
  </form>
  <button on:click={() => goto('/index')}>一覧に戻る</button>
</main>
