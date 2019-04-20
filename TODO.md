# TODO

 * SEO stuff, like
    - Canonical URLs
 * Steal more stuff from
    - https://jgthms.com/web-design-in-4-minutes/#images
    - ferd.ca
    - https://jrl.ninja/etc/1/
 * Make each blog entry its own directory, so relevant images are put
   in the same dir as the post?
 * RSS feed
 * Analytics
 * Live reload: https://www.browsersync.io
 * Watch mode
     - Do different things depending on the directory of the changed file
        - If a markdown file changes, re-render it
        - If a static file changes, copy it
        - Can be accomplished with inotify
    - Trigger hooks for post-processing?
        - https://pythonhosted.org/watchdog/
 * Image resizing
    - add a dimension to file name to create automatically - eg if
      a markdown file references “alpaca-800.png” it will look for
      “alpaca.png” in the same directory and create a resized version 
