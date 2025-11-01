<script setup>
import { ref, onMounted, watch } from 'vue';

const emit = defineEmits(['file-change']);
const props = defineProps(['fileDataUrl']);

const isSaving = ref(false);
const fileReader = new FileReader();
const fileInput = ref(null);
const file = ref(null);
const fileDataUrl = ref('');

watch(() => props.fileDataUrl, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    fileDataUrl.value = newValue;
  }
});

onMounted(() => {
  fileReader.addEventListener(
    "load",
    () => {
      fileDataUrl.value = fileReader.result;
      isSaving.value = false;
      emit("file-change", fileDataUrl.value);
    },
    false
  );
});

function fileChange(event) {
  isSaving.value = true;
  const input = event.target;
  file.value = input.files[0];
  fileReader.readAsDataURL(file.value);
}

function clickRemoveImageHandler() {
  file.value = null;
  emit("file-change", '');
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}
</script>

<template>
  <input tabindex="-1" type="file" name="uploadInput" :disabled="isSaving" @change="fileChange"
         accept="image/jpeg, image/png, image/gif" class="input-file" ref="fileInput" />
  <a class="remove-link" href="#" v-if="fileDataUrl" @click="clickRemoveImageHandler">Supprimer l'image</a>
</template>

<style scoped>
  .remove-link {
    display: block;
  }
</style>
