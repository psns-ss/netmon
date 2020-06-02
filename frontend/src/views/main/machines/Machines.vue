<template xmlns:>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Machines
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon large color="secondary" @click="this.getMachines">
        <v-icon>
          mdi-refresh
        </v-icon>
      </v-btn>

      <v-btn color="primary" to="/main/machines/create">Create Machine</v-btn>

    </v-toolbar>
    <v-data-table :headers="headers" :items="machines">
      <template slot="item" slot-scope="props">
        <tr>
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.host }}</td>
          <td>
            <v-icon v-if="props.item.was_recently_online">mdi-checkbox-marked-circle-outline</v-icon>
            <v-icon v-else>mdi-checkbox-blank-circle-outline</v-icon>
          </td>
          <td class=" layout px-0 ">
            <v-tooltip top>
              <span>Interfaces</span>
              <template v-slot:activator="{ on }">
                <v-btn large icon v-on="on" text :to="{name: 'main-machines-interfaces', params: {id: props.item.id}}">
                  <v-icon>mdi-lan</v-icon>
                </v-btn>
              </template>
            </v-tooltip>

            <v-tooltip top>
              <span>Active Processes</span>
              <template v-slot:activator="{ on }">
                <v-btn large icon v-on="on" text
                       :to="{name: 'main-machines-active-processes', params: {id: props.item.id}}">
                  <v-icon>mdi-rocket-launch</v-icon>
                </v-btn>
              </template>
            </v-tooltip>

            <v-tooltip top>
              <span>Edit</span>
              <template v-slot:activator="{ on }">
                <v-btn large icon v-on="on" text :to="{name: 'main-machines-edit', params: {id: props.item.id}}">
                  <v-icon>mdi-square-edit-outline</v-icon>
                </v-btn>
              </template>
            </v-tooltip>

            <v-tooltip top>
              <span>Delete</span>
              <template v-slot:activator="{ on }">
                <v-btn large v-on="on" icon top @click="deleteMachine(props.item.id)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-tooltip>
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
  import {Component, Vue} from 'vue-property-decorator';
  import {readMachines} from '@/store/machines/getters';
  import {dispatchGetMachines, dispatchDeleteMachine} from '@/store/machines/actions';

  @Component
  export default class Machines extends Vue {
    public headers = [
      {
        text: 'Name',
        sortable: true,
        value: 'name',
        align: 'left',
      },
      {
        text: 'Host',
        sortable: true,
        value: 'host',
        align: 'left',
      },
      {
        text: 'Was recently online',
        sortable: true,
        value: 'was_recently_online',
        align: 'left',
      },
    ];
    public timerId = 0;

    public async deleteMachine(machineId: number) {
      await dispatchDeleteMachine(this.$store, {id: machineId});
    }

    get machines() {
      return readMachines(this.$store);
    }

    public async getMachines() {
      await dispatchGetMachines(this.$store);
    }

    public async mounted() {
      await this.getMachines();
      this.timerId = setInterval(this.getMachines, 10000);
    }

    public beforeDestroy() {
      clearInterval(this.timerId);
    }
  }
</script>
