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
      <template slot="item" slot-scope="props">
        <tr>
          <td>{{ props.item.name }}</td>
          <td>{{ props.item.host }}</td>
          <td>
            <v-icon v-if="props.item.was_recently_online">mdi-checkbox-marked-circle-outline</v-icon>
            <v-icon v-else>mdi-checkbox-blank-circle-outline</v-icon>
          </td>
          <td class="justify-center layout px-0 ">
            <v-tooltip top>
              <span>Edit</span>
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" text :to="{name: 'main-machines-edit', params: {id: props.item.id}}">
                  <v-icon>mdi-square-edit-outline</v-icon>
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
      {
        text: 'Was recently online',
        sortable: true,
        value: 'was_recently_online',
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
