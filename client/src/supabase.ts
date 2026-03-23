import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://qejuledbwnxtvcjuspgu.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFlanVsZWRid254dHZjanVzcGd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQxNzUyOTksImV4cCI6MjA4OTc1MTI5OX0.AtqXr3ZFohL8PHJob_lcDe9w_RMr5JnZXZFIBzD2Lc4'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

