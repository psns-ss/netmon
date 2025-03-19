<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Machine</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Name</div>
            <div
                class="title primary--text text--darken-2"
            >{{machine.name}}
            </div>
          </div>
          <v-form
              v-model="valid"
              ref="form"
              lazy-validation
          >
            <v-text-field
                label="New Name"
                data-vv-name="name"
                v-model="name"
                required
            ></v-text-field>
            <v-text-field
                label="Host"
                data-vv-name="host"
                v-model="host"
                required
            ></v-text-field>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn
            @click="submit"
            :disabled="!valid"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import {IMachineUpdate} from '@/interfaces';
    import {readOneMachine} from '@/store/machines/getters';
    import {dispatchGetMachines, dispatchUpdateMachine} from '@/store/machines/actions';

    @Component
    export default class EditMachine extends Vue {
        public valid = true;
        public name: string = '';
        public host: string = '';

        public async mounted() {
            await dispatchGetMachines(this.$store);
            this.reset();
        }

        public reset() {
            this.name = '';
            this.host = '';
            this.$validator.reset();
            if (this.machine) {
                this.host = this.machine.host;
                this.name = this.machine.name;
            }
        }

        public cancel() {
            this.$router.back();
        }

        public async submit() {
            if (await this.$validator.validateAll()) {
                const updatedMachine: IMachineUpdate = {};
                if (this.name) {
                    updatedMachine.name = this.name;
                }
                if (this.host) {
                    updatedMachine.host = this.host;
                }
                await dispatchUpdateMachine(this.$store, {id: this.machine!.id, machine: updatedMachine});
                await this.$router.push('/main/machines');
            }
        }

        get machine() {
            return readOneMachine(this.$store)(+this.$router.currentRoute.params.id);
        }
    }
</script>
