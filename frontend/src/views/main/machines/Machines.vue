<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Machines
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/machines/create">Create Machine</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="machines">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.host }}</td>
        <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-machines-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
  import {Component, Vue} from 'vue-property-decorator';
  import {readMachines} from '@/store/machines/getters';
  import {dispatchGetMachines} from '@/store/machines/actions';

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
    ];

    get machines() {
      return readMachines(this.$store);
    }

    public async mounted() {
      await dispatchGetMachines(this.$store);
    }
  }
</script>
