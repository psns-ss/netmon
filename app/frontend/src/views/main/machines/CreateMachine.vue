<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create Machine</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Name" v-model="name" required></v-text-field>
            <v-text-field label="Host" v-model="host" required></v-text-field>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {IMachineCreate} from '@/interfaces';
import {dispatchCreateMachine, dispatchGetMachines} from '@/store/machines/actions';

@Component
export default class CreateMachine extends Vue {
  public valid = false;
  public name: string = '';
  public host: string = '';

  public reset() {
    this.name = '';
    this.host = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const machine: IMachineCreate = {
        name: this.name,
        host: this.host,
      };
      await dispatchCreateMachine(this.$store, machine);
      await this.$router.push('/main/machines');
    }
  }
  public async mounted() {
    await dispatchGetMachines(this.$store);
    this.reset();
  }
}
</script>
