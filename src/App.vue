<template>
  <div class="container mx-auto p-4 bg-gray-900 text-white min-h-screen">
    <h1 class="text-3xl font-bold mb-4">Medical Study App</h1>

    <label
      for="file-upload"
      class="
        cursor-pointer
        bg-green-500
        hover:bg-green-700
        text-white
        font-bold
        py-2
        px-4
        rounded
      "
    >
      Upload Files
    </label>
    <input
      type="file"
      id="file-upload"
      class="hidden"
      @change="handleFileUpload"
      multiple
    />

    <div v-if="processing" class="mt-4 flex items-center">
      <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-green-500 mr-2"></div>
      <p>Processing...</p>
    </div>

    <div v-if="errorMessage" class="mt-4 text-red-500">{{ errorMessage }}</div>

    <div v-if="extractedTerms" class="mt-4">
      <h2 class="text-2xl font-bold mb-2">Extracted Terms:</h2>
      <ul class="list-disc list-inside">
        <li v-for="term in extractedTerms" :key="term" class="py-1">{{ term }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      processing: false,
      extractedTerms: null,
      errorMessage: null
    };
  },
  methods: {
    async handleFileUpload(event) {
      this.processing = true;
      this.errorMessage = null; // Clear any previous errors
      const files = event.target.files;
      try {
        for (let i = 0; i < files.length; i++) {
          const file = files[i];
          const formData = new FormData();
          formData.append('file', file);

          const response = await axios.post('/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          this.extractedTerms = response.data.extracted_terms;
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        this.errorMessage = 'An error occurred during processing.';
      } finally {
        this.processing = false;
      }
    }
  }
};
</script>
