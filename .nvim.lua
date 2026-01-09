
-- 字典高亮
-- 单词 / 解释高亮

vim.api.nvim_create_autocmd("User", {
	pattern = "TSUpdate",
	callback = function()
		require("nvim-treesitter.parsers").dct_txt = {
			install_info = {
				url = "https://github.com/okxhfiweohi/dct_txt_ts.git",
				queries = "queries",
			},
		}
	end,
})
vim.api.nvim_create_autocmd({ "BufRead", "BufNewFile" }, {
	pattern = "*.dct.txt",
	callback = function()
		vim.bo.filetype = "dct_txt"
		vim.treesitter.start()
	end,
})
