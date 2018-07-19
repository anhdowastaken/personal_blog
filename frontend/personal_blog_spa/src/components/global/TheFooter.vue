<template>
  <!-- Start Footer bottom Area -->
  <footer>
    <div class="footer-area">
      <div class="container">
        <div class="row">
          <div class="col-md-6 col-sm-6 col-xs-12">
            <div class="footer-content">
              <div class="footer-head">
                <div class="footer-logo">
                  <h2><span>{{ first_name }}</span>{{ last_name }}</h2>
                </div>
                <p></p>
                <div class="footer-icons">
                  <ul>
                    <li><a target="_blank" :href="'//' + facebook_link"><i class="fa fa-facebook"></i></a></li>
                    <li><a target="_blank" :href="'//' + twitter_link"><i class="fa fa-twitter"></i></a></li>
                    <li><a target="_blank" :href="'//' + instagram_link"><i class="fa fa-instagram"></i></a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <!-- end single footer -->
          <div class="col-md-6 col-sm-6 col-xs-12">
            <div class="footer-content">
              <div class="footer-head">
                <h4>information</h4>
                <p></p>
                <div class="footer-contacts">
                  <p><span>Tel: </span>{{ phone_number }}</p>
                  <p><span>Email: </span><a :href="'mailto:' + email_address">{{ email_address }}</a></p>
                </div>
              </div>
            </div>
          </div>
          <!-- end single footer -->
        </div>
      </div>
    </div>
    <div class="footer-area-bottom">
      <div class="container">
        <div class="row">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="copyright text-center">
              <p>
                &copy; Copyright <strong>anhDO</strong>. All Rights Reserved
              </p>
            </div>
            <div class="credits">
              <!--
                All the links in the footer should remain intact.
                You can delete the links only if you purchased the pro version.
                Licensing information: https://bootstrapmade.com/license/
                Purchase the pro version with working PHP/AJAX contact form: https://bootstrapmade.com/buy/?theme=eBusiness
              -->
              Designed by <a href="https://bootstrapmade.com/">BootstrapMade</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import { facebook_link,
         twitter_link,
         instagram_link,
         first_name,
         last_name,
         phone_number,
         email_address } from '@/common'

export default {
    name: 'FooterComponent',
    components: {

    },
    data() {
        return {
            first_name: first_name,
            last_name: last_name,
            phone_number: phone_number,
            email_address: email_address,
            facebook_link: facebook_link,
            twitter_link: twitter_link,
            instagram_link: instagram_link
        }
    },
    computed: {

    }
}
</script>

<style scoped>
</style>
