<template>
  <div class="main">
    <el-button
      style="position:absolute; top: 20px; right: 20px; width: 28px; padding: 6px; box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);"
      @click="helpVisible = true"
      round
    >?</el-button>
    <div class="block">
      <div v-for="entry in tracked" v-bind:key="entry.key" class="track-card">
        <el-card>
          <div style="display: inline-block;">
            <h3>
              <span v-if="entry.strict">"</span>
              {{ entry.key
              }}
              <span v-if="entry.strict">"</span>
            </h3>
          </div>
          <el-button
            type="danger"
            icon="el-icon-delete"
            plain
            circle
            style="float: right;"
            @click="remove_track(entry.key)"
          />
          <el-button
            style="float: right; margin-right: 5px; font-size: 0.8rem; line-height: 14px; width: 28px;"
            v-text="data_lengths[entry.key] || 0"
            circle
          ></el-button>
        </el-card>
      </div>
      <div class="track-card">
        <el-card>
          <div style="display: inline-block;">
            <h3>新增</h3>
          </div>
          <el-button
            icon="el-icon-plus"
            circle
            style="float: right;"
            @click="dialogVisible = true"
          />
        </el-card>
      </div>
    </div>

    <el-dialog title="说明" :visible.sync="helpVisible" width="400px" class="help" center>
      <p>
        <b>关键词搜索：</b>
        <br />指定一些搜索条目，它们会每天更新，每次抓取
        Google 搜索中近 3 天的结果前 2 页。重复结果会被自动移除。
      </p>
      <p>
        <b>浏览：</b>
        <br />对于获取到的条目，可以点击链接查看，也可以点击按钮移除。这两种操作都会将该条目记录为“已访问”，不会再被显示。
      </p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="helpVisible = false">关闭</el-button>
      </span>
    </el-dialog>

    <el-dialog title="添加搜索条目" :visible.sync="dialogVisible" width="400px" center>
      <el-input placeholder="关键词" v-model="add_input" clearable />
      <el-popover placement="top-start" trigger="hover">
        <p>搜索结果必须包含与以上关键词完全相同的内容</p>
        <el-checkbox v-model="add_strict" slot="reference" label="严格匹配" style="margin-top: 20px;" />
      </el-popover>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submit_add" :loading="submitting">添加</el-button>
      </span>
    </el-dialog>

    <el-divider />

    <div class="block">
      <el-card
        class="entry"
        v-for="[index, entry] in data.entries()"
        v-bind:key="'entry' + index"
        v-show="entry.show"
      >
        <div slot="header">
          <el-popover placement="bottom-start" trigger="hover">
            <p>{{ entry.url }}</p>
            <el-link
              slot="reference"
              type="primary"
              @click="access(entry.key, entry.url, true)"
              v-html="entry.title"
              target="_blank"
              style="font-size: 1.2rem"
            />
          </el-popover>
          <el-button
            icon="el-icon-close"
            circle
            style="float: right;"
            @click="access(entry.key, entry.url, false)"
          />
        </div>
        <div style="width: 100%;" class="meta">
          <div style="display: inline-block; padding-right: 20px;">
            记录时间:
            {{ new Date(entry.date + "+00:00").toLocaleString("ja-JP") }}
          </div>
          <div style="display: inline-block;">来源: {{ trim_url(entry.url) }}</div>
        </div>
        <p v-html="entry.snippet"></p>
      </el-card>
    </div>
  </div>
</template>

<style>
.el-button.is-circle {
  padding: 6px !important;
}
.el-popover {
  max-width: 650px;
}
.el-dialog,
.el-input__inner,
.el-checkbox,
.el-checkbox__inner,
.el-button,
.el-popover,
.el-card {
  border-radius: 14px !important;
}
.el-button--default,
.el-card,
.el-popover {
  background-color: rgba(255, 255, 255, 0.9) !important;
}
.el-button,
.el-input__inner {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}
.el-dialog {
  background-color: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(4px);
}
p {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
</style>

<style scoped>
.main {
  text-align: left;
  min-width: 480px;
  max-width: 760px;
  margin: auto;
}
.block {
  padding: 0 20px;
}
.track-card {
  box-sizing: border-box;
  display: inline-block;
  width: 50%;
  margin-top: 20px;
}
.track-card:nth-child(odd) {
  padding-right: 10px;
}
.track-card:nth-child(even) {
  padding-left: 10px;
}
.entry {
  margin-bottom: 20px;
}
.meta {
  margin-top: 0;
  color: #888888;
  margin-bottom: 20px;
}
.help p {
  margin-bottom: 0.5rem;
}
h3 {
  margin: 0;
}
p {
  color: #111111;
  margin: 0;
}
</style>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String
  },
  data: function() {
    return {
      data: [],
      add_input: "",
      add_strict: false,
      dialogVisible: false,
      helpVisible: false,
      submitting: false,
      tracked: []
    };
  },
  computed: {
    data_lengths: function() {
      let result = {};
      for (let i = 0; i < this.data.length; i++) {
        let item = this.data[i];
        if (!item.show) {
          continue;
        }
        if (result[item.key]) {
          result[item.key] += 1;
        } else {
          result[item.key] = 1;
        }
      }
      return result;
    }
  },
  methods: {
    // Notify backend that one url is clicked (or ignored)
    access: function(key, url, go) {
      this.$http
        .get(this.$backend + "/access", {
          params: {
            key,
            url
          }
        })
        .then(() => {
          let index = this.data.findIndex(entry => entry.url == url);
          let entry = this.data[index];
          entry.show = false;
          this.$set(this.data, index, entry);
        });
      if (go) {
        window.open(url, "_blank");
      }
    },
    // Keep domain from a url
    trim_url: function(url) {
      return new URL(url).hostname;
    },
    update_tracked: function() {},
    submit_add: function() {
      this.submitting = true;
      this.$http
        .get(this.$backend + "/add", {
          params: {
            key: this.add_input,
            strict: this.add_strict
          }
        })
        .then(this.load_data)
        .then(() => {
          this.submitting = false;
          this.dialogVisible = false;
        });
    },
    load_data: function() {
      let fetch_entries = this.$http.get(this.$backend).then(response => {
        this.data = response.data.data;
        for (let i = 0; i < this.data.length; i++) {
          this.data[i].show = true;
          this.data[i].snippet = (this.data[i].snippet || "")
            .replace(/\s+/g, " ")
            .replace(new RegExp(this.data[i].key, "ig"), "<b>$&</b>");
          this.data[i].title = this.data[i].title
            .replace(/\s+/g, " ")
            .replace(new RegExp(this.data[i].key, "ig"), "<b>&nbsp;$&&nbsp;</b>");
        }
        console.log(this.data);
      });
      let fetch_tracked = this.$http
        .get(this.$backend + "/ls")
        .then(response => {
          this.tracked = response.data.data;
          console.log(this.tracked);
        });
      return Promise.all([fetch_entries, fetch_tracked]);
    },
    remove_track: function(key) {
      this.$http
        .get(this.$backend + "/remove", {
          params: {
            key
          }
        })
        .then(this.load_data);
    }
  },
  mounted: function() {
    this.$backend = "http://" + window.location.hostname + ":8000";
    this.load_data();
  }
};
</script>
