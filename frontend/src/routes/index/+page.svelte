<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import {
    Input,
    Label,
    Button,
    Modal,
    AccordionItem,
    Accordion,
    Textarea,
    Radio,
    Spinner,
    ButtonGroup,
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    GradientButton,
    Popover
  } from 'flowbite-svelte'

  let title = '';
  let description = '';
  let voiceFile = null;
  let message = writable('');
  let audios = writable([]);
  let editMode = writable(null); // 現在編集モードの音声ファイルのID
  let advice = writable('');
  let showModal = false;  // モーダルの表示状態を管理するスト
  let loadingSource = false

  // 音声ファイルをアップロードする処理
  async function uploadAudio() {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('voice', voiceFile);

    const token = localStorage.getItem('authToken');

    if (!token) {
      console.log("Token not found or undefined:", token);
      message.set('You must be logged in to upload audio.');
      return;
    }

    console.log("Using token:", token); // トークンを取得したことを確認

    try {
      const response = await fetch('http://localhost:8000/api/audio/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,  // トークンをヘッダーに追加
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        message.set('Audio upload successful.');
        await fetchUserAudios();  // アップロード後に最新のリストをフェッチ
        // フォームのリセット
        title = '';
        description = '';
        voiceFile = null;
      } else {
        message.set(`Upload failed: ${JSON.stringify(data)}`);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      message.set(`Fetch error: ${error}`);
    }
  }

// ユーザーの音声ファイルを取得する処理
  async function fetchUserAudios() {
    const token = localStorage.getItem('authToken');

    try {
      const response = await fetch('http://localhost:8000/api/audio/', {
        method: 'GET',
        headers: {
          'Authorization': `Token ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        console.log("response.ok");
        console.log("data: "+ JSON.stringify(data));
        audios.set(data);
      } else {
        message.set(`Failed to fetch audios: ${JSON.stringify(data)}`);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      message.set(`Fetch error: ${error}`);
    }
  }

  // 音声ファイルを更新する関数
  async function updateAudio(audio) {
    const formData = new FormData();
    formData.append('title', audio.title);
    formData.append('description', audio.description);
    if (audio.newVoice) {
      formData.append('voice', audio.newVoice);  // 新しい音声ファイルが指定されている場合
    }

    const token = localStorage.getItem('authToken');

    if (!token) {
      message.set('You must be logged in to update audio.');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/audio/${audio.id}/`, {
        method: 'PUT',
        headers: {
          'Authorization': `Token ${token}`,  // トークンをヘッダーに追加
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        message.set('Audio update successful.');
        await fetchUserAudios();  // 更新後に最新のリストをフェッチ
        editMode.set(null);  // 編集モードを終了
      } else {
        message.set(`Update failed: ${JSON.stringify(data)}`);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      message.set(`Fetch error: ${error}`);
    }
  }


  // 音声ファイルを削除する関数
  async function deleteAudio(audioId) {
    const token = localStorage.getItem('authToken');

    if (!token) {
      message.set('You must be logged in to delete audio.');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/audio/${audioId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${token}`,  // トークンをヘッダーに追加
        },
      });

      if (response.ok) {
        message.set('Audio deleted successfully.');
        await fetchUserAudios();  // 削除後に最新のリストをフェッチ
      } else {
        const data = await response.json();
        message.set(`Delete failed: ${JSON.stringify(data)}`);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      message.set(`Fetch error: ${error}`);
    }
  }

  async function transcribeAndGetAdvice(audioId) {
    const token = localStorage.getItem('authToken');

    if (!token) {
      message.set('You must be logged in to get advice.');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/audio/${audioId}/transcribe_and_advice/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        advice.set(data.advice);
        message.set('Successfully retrieved advice.');
        console.log("data.advice: "+ data.advice);
        showModal = true;  // モーダルを表示する
      } else {
        message.set(`Failed to get advice: ${JSON.stringify(data)}`);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      message.set(`Fetch error: ${error}`);
    }
  }

  function closeModal() {
    showModal = false;
  }

  // 初回のトークン確認
  onMount(async () => {
    const token = localStorage.getItem('authToken');
    console.log("Token retrieved on mount:", token);  // マウント時にトークンが取得されているか確認
    if (!token) {
      message.set('You must be logged in to view this page.');
    } else {
      await fetchUserAudios();
    }
  });

  let defaultModal = true;
</script>

<main class="bg-gray-100 min-h-screen">
  <h1>Your Audio Files</h1>

  <!-- 音声ファイルのリスト -->
  <section class="">
    <h2>Audio List</h2>
    <ul>
      {#each $audios as audio}
        <li>
          {#if $editMode === audio.id}
            <!-- 編集モード -->
            <div>
              <label for="edit-title-{audio.id}">Title:</label>
              <input type="text" id="edit-title-{audio.id}" bind:value={audio.title} />

              <label for="edit-description-{audio.id}">Description:</label>
              <textarea id="edit-description-{audio.id}" bind:value={audio.description}></textarea>

              <label for="edit-voice-{audio.id}">Voice File (optional):</label>
              <input type="file" id="edit-voice-{audio.id}" accept="audio/*" on:change={e => audio.newVoice = e.target.files[0]} />

              <button on:click={() => updateAudio(audio)}>Update</button>
              <button on:click={() => editMode.set(null)}>Cancel</button>
            </div>
          {:else}
            <!-- 表示モード -->
            <h3>{audio.title}</h3>
            <p>{audio.description}</p>
            <audio controls>
              <source src={audio.voice} type="audio/mp4" />
              <source src={audio.voice} type="audio/mpeg" /> <!-- .mp3 ファイルのため -->
              <source src={audio.voice} type="audio/ogg" />  <!-- .ogg ファイルのため -->
              Your browser does not support the audio element.
            </audio>
            <button on:click={() => transcribeAndGetAdvice(audio.id)}>Get Advice</button>
            <button on:click={() => editMode.set(audio.id)}>Edit</button>
            <button on:click={() => deleteAudio(audio.id)}>Delete</button>  <!-- 削除ボタンを追加 -->
          {/if}
        </li>
      {/each}
    </ul>
  </section>

  <!-- 音声ファイルのアップロードフォーム -->
  <section class="">
    <h2>Upload New Audio</h2>
    <div>
      <label for="title">Title:</label>
      <input type="text" id="title" bind:value={title} placeholder="Enter title" />
    </div>
    <div>
      <label for="description">Description:</label>
      <textarea id="description" bind:value={description} placeholder="Enter description"></textarea>
    </div>
    <div>
      <label for="voice">Voice File:</label>
      <input type="file" id="voice" accept="audio/*" on:change={e => voiceFile = e.target.files[0]} />
    </div>
    <button on:click={uploadAudio}>Upload</button>
  </section>

  <p>{$message}</p>
  {#if showModal}
    <div class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-xl w-full relative">
        <button class="absolute top-0 right-0 m-4 text-gray-600" on:click={closeModal}>✖️</button>
        <h2 class="text-2xl font-bold mb-4">AIによる改善案</h2>
        {#if loadingSource}
          <Spinner size="10" currentFill="#1AE9D0" currentColor="#964FF3" />
        {:else if !loadingSource && !advice}
          <p>アドバイスが得られませんでした</p>
        {:else if advice}
          <p>{$advice}</p>
        {/if}
        <button class="bg-gray-600 text-white px-4 py-2 rounded w-full" on:click={closeModal}>とじる</button>
      </div>
    </div>
  {/if}

</main>


<style>
    .video-card {
    transition: transform 0.3s;
  }

  .video-card:hover {
    transform: scale(1.05);
  }


  textarea,
  input[type="file"] {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  button {
    display: inline-block;
    padding: 0.75rem 1.25rem;
    color: white;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background-color: #0056b3;
  }
</style>