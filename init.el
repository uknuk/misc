;; additional packages which are configured here
(setq package-list '(solarized-theme
                     geiser
                     sr-speedbar
                     neotree
                     web-mode
                     highlight-indentation))

(setq package-archives '(("gnu" . "https://elpa.gnu.org/packages/")
                         ("melpa" . "http://melpa.org/packages/")
                         ("marmalade" . "http://marmalade-repo.org/packages/")))

(package-initialize)

(unless package-archive-contents
  (package-refresh-contents))

(dolist (package package-list)
  (unless (package-installed-p package)
    (package-install package)))

(add-to-list 'load-path "~/.emacs.d/lisp")

(load-theme 'solarized-dark t)

(setq-default tab-width 2)
(setq-default indent-tabs-mode nil)

(setq column-number-mode 1)
(tool-bar-mode -1)
(setq inhibit-startup-screen t)
(setq custom-file "~/.emacs.d/lisp/custom.el")

(cond ((eq system-type 'darwin)
       (when (memq window-system '(mac ns))
           (exec-path-from-shell-initialize))
      (require 'emulate-mac-keyboard-mode)
      (setq emulate-mac-finnish-keyboard-mode t)
      (setq mac-right-option-modifier nil)
      (setq geiser-guile-binary "/usr/local/bin/guile"))
      ((eq system-type 'gnu-linux)
       (setq geiser-guile-binary "/usr/bin/geiser")))

(setq sr-speedbar-auto-refresh nil)
(setq speedbar-show-unknown-files t)
(setq scss-compile-at-save nil)

(setq js-indent-level 2)
(setq jsx-indent-level 2)
(setq c-basic-offset 2)
(setq css-indent-offset 2)

(add-to-list 'auto-mode-alist '("\\.erb\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.html?\\'" . web-mode))

(defun my-web-mode-hook () "Hooks for Web mode."
       (setq web-mode-markup-indent-offset 2)
       (setq web-mode-html-offset 2)
       (setq web-mode-css-indent-offset 2)
       (setq web-mode-code-indent-offset 2)
       )

(add-hook 'web-mode-hook 'my-web-mode-hook)
(add-hook 'ruby-mode-hook #'rubocop-mode)

(add-to-list 'auto-mode-alist '("\\.jsx$" . web-mode))
(defadvice web-mode-highlight-part (around tweak-jsx activate)
  (if (equal web-mode-content-type "jsx")
      (let ((web-mode-enable-part-face nil))
        ad-do-it)
    ad-do-it))

(defvar my-term-shell "/bin/bash")
(defadvice ansi-term (before force-bash)
  (interactive (list my-term-shell)))
(ad-activate 'ansi-term)

(unless (version<= emacs-version "24.4")
  (defun delete-extra-blanks ()
    (interactive)
    (delete-duplicate-lines (region-beginning) (region-end) nil t)))

(add-hook 'before-save-hook
          (lambda ()
            (untabify (point-min) (point-max))
            (delete-trailing-whitespace)
            (unless (version<= emacs-version "24.4")
              (delete-duplicate-lines (point-min) (point-max) nil t))))

; finally keyboard shortcuts
(global-set-key (kbd "C-c t") 'ansi-term)
(global-set-key (kbd "C-c i") 'indent-region)
(global-set-key (kbd "C-c c") 'comment-region)
(global-set-key (kbd "C-c u") 'uncomment-region)
(global-set-key (kbd "C-c h") 'highlight-indentation-mode)
(global-set-key (kbd "C-c l") 'linum-mode)
(global-set-key (kbd "C-c w") 'whitespace-mode)
(global-set-key (kbd "C-c s") 'sr-speedbar-toggle)
(global-set-key (kbd "C-c n") 'neotree)
(global-set-key (kbd "C-c p") 'list-packages)
