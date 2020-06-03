<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Active Processes of machine "{{machineName || "Unnamed"}}"
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon large color="secondary" @click="$router.back()">
        <v-icon>
          mdi-chevron-left
        </v-icon>
      </v-btn>

      <v-btn icon large color="secondary" @click="this.refreshActiveProcesses">
        <v-icon>
          mdi-refresh
        </v-icon>
      </v-btn>
    </v-toolbar>

    <v-data-table :headers="headers" :items="activeProcesses">
      <template slot="item" slot-scope="props">
        <tr>
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.id }}</td>
          <td>{{ props.item.path }}</td>
          <td>{{ props.item.hash }}</td>
          <td>
            <v-icon color="red" v-if="!props.item.is_hash_same">mdi-alert</v-icon>
            <v-icon v-else>mdi-check</v-icon>
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
  import {Component, Vue} from 'vue-property-decorator';
  import {readMachineActiveProcesses, readOneMachine} from '@/store/machines/getters';
  import {dispatchGetMachine, dispatchGetMachineActiveProcesses} from '@/store/machines/actions';

  @Component
  export default class MachinesActiveProcesses extends Vue {
    public headers = [
      {
        text: 'Name',
        sortable: true,
        value: 'name',
        align: 'left',
      },
      {
        text: 'Id',
        sortable: true,
        value: 'id',
        align: 'left',
      },
      {
        text: 'Path',
        sortable: true,
        value: 'path',
        align: 'left',
      },
      {
        text: 'Hash',
        value: 'hash',
        align: 'left',
      },
      {
        text: 'Hash Changed',
        value: '!is_hash_same',
        align: 'left',
      },

    ];

    public timerId = 0;

    get machineName() {
      const machine = readOneMachine(this.$store)(+this.$router.currentRoute.params.id);
      return machine?.name;
    }

    get activeProcesses() {
      return readMachineActiveProcesses(this.$store);
    }

    public async refreshActiveProcesses() {
      await dispatchGetMachineActiveProcesses(this.$store, {id: +this.$router.currentRoute.params.id});
    }

    public async mounted() {
      await dispatchGetMachine(this.$store, {id: +this.$router.currentRoute.params.id});
      await this.refreshActiveProcesses();
      this.timerId = setInterval(this.refreshActiveProcesses, 10000);
    }


    public beforeDestroy() {
      clearInterval(this.timerId);
    }
  }
</script>
