<template>
  <transition name="modal">
    <div class="modal fade" role="dialog"
         v-bind:style="{ display: notificationDisplayStyle }"
         v-bind:class="{ in: notificationDisplay }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" v-on:click.stop.prevent="hideNotification">&times;</button>
            <h4 class="modal-title">{{ this.notificationHeader }} </h4>
          </div>
          <div class="modal-body" style="white-space: pre-line;">
            <p>{{ this.notificationBody }}</p>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'

export default {
    name: 'Notification',
    data() {
        return {

        }
    },
    computed: mapState({
        notificationHeader: state => state.notificationHeader,
        notificationBody: state => state.notificationBody,
        notificationDisplay: state => state.notificationDisplay,
        notificationDisplayStyle: state => state.notificationDisplayStyle,
        notificationRedirectAfterClose: state => state.notificationRedirectAfterClose,
        notificationRedirectComponentName: state => state.notificationRedirectComponentName
    }),
    methods: {
        ...mapMutations([
            'hideNotification'
        ])
    }
}
</script>

<style scoped>
</style>
