<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Interfaces of machine "{{machineName || "Unnamed"}}"
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon large color="secondary" @click="$router.back()">
        <v-icon>
          mdi-chevron-left
        </v-icon>
      </v-btn>

      <v-btn icon large color="secondary" @click="this.refreshMachineInterfaces">
        <v-icon>
          mdi-refresh
        </v-icon>
      </v-btn>
    </v-toolbar>

    <v-data-table :headers="headers" :items="interfaces">
      <template slot="item" slot-scope="props">
        <tr>
          <td>{{ props.item.interface_description }}</td>
          <td>{{ props.item.ipv4_address }}</td>
          <td>{{ props.item.ipv4_default_gateway }}</td>
          <td>{{ props.item.dns_server }}</td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
  import {Component, Vue} from 'vue-property-decorator';
  import {readMachineInterfaces, readOneMachine} from '@/store/machines/getters';
  import {dispatchGetMachine, dispatchGetMachineInterfaces} from '@/store/machines/actions';

  @Component
  export default class MachinesInterfaces extends Vue {
    public headers = [
      {
        text: 'InterfaceDescription',
        sortable: true,
        value: 'interface_description',
        align: 'left',
      },
      {
        text: 'IPv4Address',
        sortable: true,
        value: 'ipv4_address',
        align: 'left',
      },
      {
        text: 'IPv4DefaultGateway',
        sortable: true,
        value: 'ipv4_default_gateway',
        align: 'left',
      },
      {
        text: 'DNSServer',
        sortable: true,
        value: 'dns_server',
        align: 'left',
      },
    ];

    public timerId = 0;

    get machineName() {
      const machine = readOneMachine(this.$store)(+this.$router.currentRoute.params.id);
      return machine?.name;
    }

    get interfaces() {
      return readMachineInterfaces(this.$store);
    }

    public async refreshMachineInterfaces() {
      await dispatchGetMachineInterfaces(this.$store, {id: +this.$router.currentRoute.params.id});
    }

    public async mounted() {
      await dispatchGetMachine(this.$store, {id: +this.$router.currentRoute.params.id});
      await this.refreshMachineInterfaces();
      this.timerId = setInterval(this.refreshMachineInterfaces, 10000);
    }

    public beforeDestroy() {
      clearInterval(this.timerId);
    }
  }

</script>
