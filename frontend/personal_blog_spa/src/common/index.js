import { md5 } from "@/utils";

const key_prefix = 'FxXRJTu7skv5OW0uD3xr'
export const key_jwt = key_prefix + '_jwt'
export const key_user_data = key_prefix + '_user_data'
export const recaptcha_data_sitekey = '6LeNYWQUAAAAAAzFW3De0_Jow8rF4z7pkPrSOUtH'

export const title2 = 'a simple guy'
export const title3 = 'with complicated feelings'

export const first_name = 'anh'
export const last_name = 'DO'
export const phone_number = '+84 975 730 526'
export const email_address = 'doducanh2710@gmail.com'
export const profile = 'Welcome to my blog!<br/>I\'m a software engineer in Hanoi, Vietnam. You can also find me on Facebook, Twitter, Instagram and Github.<br/>Thank you for visiting!'
export var avatar = 'https://www.gravatar.com/avatar/' + md5(email_address) + '?d=identicon&s=230'

export const facebook_link = 'facebook.com/anhdowastaken'
export const twitter_link = 'twitter.com/anhdowastaken'
export const instagram_link = 'instagram.com/anhdowastaken'
export const github_link = 'github.com/anhdowastaken'
